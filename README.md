<img width="3188" height="1202" alt="frame (3)" src="https://github.com/user-attachments/assets/517ad8e9-ad22-457d-9538-a9e62d137cd7" />


# NOKKI IRUNNONAM 🎯


## Basic Details
### Team Name: Dual Core


### Team Members
- Team Lead: Sian Soj - College of engineering perumon
- Member 2: Vighnesh V Gopal - College of engineering perumon

### Project Description
This device basically makes sure you see the loading screen all the way till the end of the loading. Yeah basically you cant believe on your childhood myth where not looking on the screen will load it faster :)
This project uses face-tracking technology to detect when the user is looking at the screen and only loads the webpage or software when proper eye contact is maintained. If the user looks away, the system pauses or hides the content, encouraging focus and reducing distractions hehe.

### The Problem (that doesn't exist)
Remember when we’d look away from the loading screen thinking it’d load faster? This project turns that superstition into reality—blink or look away, and it stops loading!"

### The Solution (that nobody asked for)
No looking away this time — the loading screen is too good to miss 😎✨

## Technical Details
### Technologies/Components Used
For Software:
Languages used
For Software:
Languages used

Python 3.x: The core language for the desktop application, handling all logic, computer vision, and GUI.
C++/Wiring: The language used for programming the Arduino microcontroller.

Frameworks used
Tkinter: A standard Python GUI framework used to build the user-facing application window, progress bar, and status labels.

Libraries used
OpenCV (cv2): For real-time computer vision tasks, including accessing the webcam and implementing face/eye detection with Haar Cascades.
pySerial: To establish and manage serial communication between the Python script and the Arduino board.
psutil: For cross-platform system process monitoring, used to detect when a web browser is opened or closed.
threading: To run the camera detection and serial communication loops in background threads, ensuring the GUI remains responsive.
subprocess: To execute external system commands, specifically for running the .bat script to close the web browser.

Tools used
IDE/Text Editor: Visual Studio Code, PyCharm, or a similar editor for Python development.
Arduino IDE: For writing, compiling, and uploading the sketch to the Arduino microcontroller.
Git & GitHub: For version control and repository management (standard practice).

For Hardware:
List Main Components
- Microcontroller: Arduino Uno R3
- LEDs x2
- LDR sensor

List specification
Microcontroller: Arduino Uno R3 (ATmega328P, 5V logic level, 16 MHz clock speed).
Webcam: Minimum resolution of 640x480 for reliable face detection.
Serial Communication: 9600 baud rate.

- List tools required
USB Type A to Type B cable: To connect the Arduino to the computer for programming and communication.
Breadboard: for prototyping

### Implementation
For Software:
### Installation

Clone the Repository:
Download and place the project files in a single directory.

(Recommended) Create a Virtual Environment:
Open a terminal in the project directory and run:

Bash

python -m venv venv
venv\Scripts\activate
Install Dependencies:
Install all the required Python libraries with a single command:

Bash

pip install opencv-python pyserial psutil
Run

Connect Hardware: Ensure the Arduino board is connected to the computer via USB.

Verify File Paths: Open the Python script and verify that the absolute path to your test.bat file is correct.

Execute the Script:
Run the main application from your terminal:

Bash

python main.py
### Project Documentation
For Software:

# Screenshots 
<img width="1920" height="1080" alt="Screenshot 2025-08-09 082122" src="https://github.com/user-attachments/assets/5f72606d-d89b-4c70-b588-5bb9c51c18ec" />
Image 1 (Looking at screen)
System detects focus — face is directly in front of the camera, maintaining the 'Focused ✅' status and keeping the distraction count at zero.

<img width="1920" height="1080" alt="Screenshot 2025-08-09 082141" src="https://github.com/user-attachments/assets/045f379a-6519-4b77-9c1b-bb3a47c591f6" />
Image 2 (Looking away)
System detects distraction — face is not aligned with the screen, triggering the 'Distracted ❌' status and increasing the distraction count.

![arduino](https://github.com/user-attachments/assets/a5b34f8a-03dc-45c2-a71b-06fb8c540190)
Arduino-based light monitoring module — using an LDR and LED indicators to detect room lighting conditions and communicate with the focus detection system for automatic loader reset in darkness

# Schematic & Circuit
<img width="1030" height="762" alt="file_2025-08-09_03 22 38" src="https://github.com/user-attachments/assets/e7c9c32e-3bf5-4ef9-aa5c-d3dc29bd9998" />
LDR → one side to 5V, other side to A0 and 10kΩ to GND; Red LED anode via 220Ω to D12, cathode to GND; Green LED anode via 220Ω to D13, cathode to GND; Arduino 5V to breadboard +, GND to breadboard –.

# Build Photos
Components
![components](https://github.com/user-attachments/assets/ba6e73ad-6277-460d-8ad2-f3d0da49c5c7)
Arduino Uno with USB cable, breadboard, jumper wires, red & green LEDs, resistors, and an LDR module for light detection.

Process
![process](https://github.com/user-attachments/assets/1e15bcf9-9051-41ee-aa8c-dcf4197bb75a)
Connecting LEDs with resistors to the Arduino Uno on a breadboard as part of the light detection and indicator circuit setup.

Final Connection
![arduino](https://github.com/user-attachments/assets/e1766e0c-a080-452f-bdbf-cc38823f67f8)
Fully assembled Arduino Uno with LDR and dual-LED indicator circuit, actively detecting ambient light levels and signaling status.

### Project Demo
# Video
https://drive.google.com/file/d/1a6AUWubB1JMmX5QQKGh7gqcDCZbs9REf/view?usp=drivesdk
A small overview at how this device works........

# Additional Demos
>Future applications
. Driver Drowsiness Detection – Alerts drivers when they blink excessively or lose focus, helping prevent accidents.
' Adaptive Lighting Systems – Automatically adjust room or screen brightness based on LDR readings for comfort and energy efficiency.
' Exam Integrity Systems – Monitor candidates' gaze and environment to prevent cheating in online/offline exams.

## Team Contributions
Sian Soj – Integrated and developed both hardware and software components, ensuring smooth interaction between sensors, Arduino, and the overall system.
Vighnesh V Gopal – Designed and implemented the frontend and backend using Python, enabling user interaction, data processing, and visual feedback.

Made with ❤️ at TinkerHub Useless Projects 

![Static Badge](https://img.shields.io/badge/TinkerHub-24?color=%23000000&link=https%3A%2F%2Fwww.tinkerhub.org%2F)
![Static Badge](https://img.shields.io/badge/UselessProjects--25-25?link=https%3A%2F%2Fwww.tinkerhub.org%2Fevents%2FQ2Q1TQKX6Q%2FUseless%2520Projects)



