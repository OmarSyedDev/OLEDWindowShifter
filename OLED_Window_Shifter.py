import win32gui
import win32con
import win32api
import random
import time
import threading
import tkinter as tk

running = False
dx = 1
dy = 1
step_size = 1
interval = 10

def is_maximized(hwnd):
    try:
        placement = win32gui.GetWindowPlacement(hwnd)
        return placement[1] == win32con.SW_MAXIMIZE
    except:
        return False

def get_windows():
    windows = []

    def enum_handler(hwnd, _):
        if not win32gui.IsWindowVisible(hwnd):
            return
        if win32gui.IsIconic(hwnd):
            return
        if is_maximized(hwnd):
            return
        title = win32gui.GetWindowText(hwnd)
        if not title:
            return
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
        if not (style & win32con.WS_OVERLAPPEDWINDOW):
            return
        try:
            win32gui.GetWindowRect(hwnd)
        except:
            return
        windows.append(hwnd)

    win32gui.EnumWindows(enum_handler, None)
    return windows

def choose_new_direction():
    global dx, dy
    screen_w = win32api.GetSystemMetrics(0)
    screen_h = win32api.GetSystemMetrics(1)
    windows = get_windows()
    while True:
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        if dx == 0 and dy == 0:
            continue
        valid = True
        for hwnd in windows:
            try:
                x, y, r, b = win32gui.GetWindowRect(hwnd)
            except:
                continue
            w = r - x
            h = b - y
            if (x <= 0 and dx < 0) or (y <= 0 and dy < 0) or \
               (x + w >= screen_w and dx > 0) or (y + h >= screen_h and dy > 0):
                valid = False
                break
        if valid:
            break
    print("New direction:", dx, dy)

def move_loop():
    global running, dx, dy
    choose_new_direction()

    while running:
        windows = get_windows()
        if not windows:
            time.sleep(interval)
            continue

        screen_w = win32api.GetSystemMetrics(0)
        screen_h = win32api.GetSystemMetrics(1)

        # --- Step 1: Fix windows out-of-bounds ---
        for hwnd in windows:
            try:
                x, y, r, b = win32gui.GetWindowRect(hwnd)
            except:
                continue
            w = r - x
            h = b - y
            new_x = min(max(x, 0), screen_w - w)
            new_y = min(max(y, 0), screen_h - h)
            if new_x != x or new_y != y:
                try:
                    win32gui.SetWindowPos(
                        hwnd, None, new_x, new_y, 0, 0,
                        win32con.SWP_NOSIZE | win32con.SWP_NOZORDER
                    )
                except:
                    continue

        # --- Step 2: Check if movement would hit an edge ---
        hit_edge = False
        for hwnd in windows:
            try:
                x, y, r, b = win32gui.GetWindowRect(hwnd)
            except:
                continue
            w = r - x
            h = b - y
            if (x + dx * step_size < 0 and dx < 0) or \
               (y + dy * step_size < 0 and dy < 0) or \
               (x + w + dx * step_size > screen_w and dx > 0) or \
               (y + h + dy * step_size > screen_h and dy > 0):
                hit_edge = True
                break

        if hit_edge:
            choose_new_direction()
            time.sleep(interval)
            continue

        # --- Step 3: Move all windows ---
        for hwnd in windows:
            try:
                x, y, r, b = win32gui.GetWindowRect(hwnd)
                win32gui.SetWindowPos(
                    hwnd, None, x + dx * step_size, y + dy * step_size,
                    0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOZORDER
                )
            except:
                pass

        time.sleep(interval)

def start():
    global running, step_size, interval
    if running:
        return
    try:
        step_size = int(step_entry.get())
        interval = float(interval_entry.get())
    except:
        print("Invalid settings, using defaults")
    running = True
    print("Starting movement")
    t = threading.Thread(target=move_loop)
    t.daemon = True
    t.start()

def stop():
    global running
    running = False
    print("Stopped")

# --- GUI ---
root = tk.Tk()
root.title("OLED Window Shifter")
root.configure(bg="black")  # Pitch-black background
root.geometry("290x150")
root.state('iconic')  # Launches the window minimized

tk.Label(root, text="Pixel Step Size", bg="black", fg="white").pack()
step_entry = tk.Entry(root, bg="black", fg="white", insertbackground="white")
step_entry.insert(0, "1")
step_entry.pack()

tk.Label(root, text="Time Between Moves (seconds)", bg="black", fg="white").pack()
interval_entry = tk.Entry(root, bg="black", fg="white", insertbackground="white")
interval_entry.insert(0, "10")
interval_entry.pack()

tk.Button(root, text="Start", command=start, bg="black", fg="white", activebackground="grey", activeforeground="white").pack(pady=5)
tk.Button(root, text="Stop", command=stop, bg="black", fg="white", activebackground="grey", activeforeground="white").pack(pady=5)

# --- Start movement automatically on launch ---
start()

root.mainloop()
