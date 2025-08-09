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

# Screenshots (Add at least 3)
![Screenshot1](Add screenshot 1 here with proper name)
*Add caption explaining what this shows*

![Screenshot2](Add screenshot 2 here with proper name)
*Add caption explaining what this shows*

![Screenshot3](Add screenshot 3 here with proper name)
*Add caption explaining what this shows*

# Diagrams
![Workflow](Add your workflow/architecture diagram here)
*Add caption explaining your workflow*

For Hardware:

# Schematic & Circuit
![Circuit](Add your circuit diagram here)
*Add caption explaining connections*

![Schematic](Add your schematic diagram here)
*Add caption explaining the schematic*

# Build Photos
![Components](Add photo of your components here)
*List out all components shown*

![Build](Add photos of build process here)
*Explain the build steps*

![Final](Add photo of final product here)
*Explain the final build*

### Project Demo
# Video
[Add your demo video link here]
*Explain what the video demonstrates*

# Additional Demos
[Add any extra demo materials/links]

## Team Contributions
- [Name 1]: [Specific contributions]
- [Name 2]: [Specific contributions]
- [Name 3]: [Specific contributions]

---
Made with ❤️ at TinkerHub Useless Projects 

![Static Badge](https://img.shields.io/badge/TinkerHub-24?color=%23000000&link=https%3A%2F%2Fwww.tinkerhub.org%2F)
![Static Badge](https://img.shields.io/badge/UselessProjects--25-25?link=https%3A%2F%2Fwww.tinkerhub.org%2Fevents%2FQ2Q1TQKX6Q%2FUseless%2520Projects)



