# OLEDWindowShifter
A Windows 11 program used to reduce burn in potential on OLED monitors.

<img width="254" height="163" alt="WindowView" src="https://github.com/user-attachments/assets/978f2f50-067e-4945-b676-41184a74f4c5" />

# What It Does
The program is designed to move all windows in the same direction until one hits the screen boundary, at which it will choose a new random direction to move the windows. The idea is that by periodically shifting windows, you can reduce the potential for burn-in on OLED monitors.

# How To Build and Run It
1. Download the OLED_Window_Shifter.py file from this repo.
2. Install Python from the official source.
3. Using command prompt, install pyinstaller:
```
pip install pyinstaller
```
3. Using command prompt, build the program using the OLED_Window_Shifter.py file (replace "path-to-file.py" below with the actual path to the OLED_Window_Shifter.py file you downloaded in step 1):
```
pyinstaller --onefile --noconsole "path-to-file.py"
```
4. Navigate to the following path in file explorer. This is where pyinstaller should have saved the .exe file you just built:
```
%USERPROFILE%\dist
```
5. Launch the OLED_Window_Shifter.exe file you just built.

# How To Use It
Launch the program. It will start minimized and with window shifting enabled (using the default values of Pixel Step Size of 1 and Time Between Moves of 10 seconds). Once launched, you can click the icon in your taskbar to see the window in case you would like to adjust pixel step size or time between moves (To do this, you must first click the stop button, adjust the the values, then click the start button). 

## Disclaimer

This repository is provided for educational and research purposes only. The authors do not provide legal advice, and by using this repository, you agree to use the information responsibly and ethically. 
The content is offered "as-is" without any warranties. The authors and contributors are not liable for any damages resulting from the use of this repository. Always ensure you have proper authorization before conducting any testing or experimentation.
