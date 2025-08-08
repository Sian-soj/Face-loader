import cv2
import tkinter as tk
from tkinter import ttk
import serial
import time
import threading

# ---------- Arduino Serial Setup ----------
# Change 'COM3' to your Arduino's port (Windows: COMx, Mac/Linux: '/dev/ttyUSB0')
try:
    arduino = serial.Serial('COM7', 9600, timeout=1)
    time.sleep(2)  # wait for Arduino to reset
except:
    arduino = None
    print("⚠️ No Arduino connected. Running without hardware.")

# ---------- Face Detection Setup ----------
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)

# ---------- Tkinter GUI Setup ----------
root = tk.Tk()
root.title("Focus Loader")
root.geometry("400x150")

label_status = tk.Label(root, text="Status: Waiting...", font=("Arial", 14))
label_status.pack(pady=10)

progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress.pack(pady=10)

progress_value = 0
progress_max = 100
focus_detected = False

# ---------- Logic ----------
def detect_face():
    global progress_value, focus_detected

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) > 0:  # Face detected
            focus_detected = True
            if arduino:
                arduino.write(b"1")  # Send '1' to Arduino
        else:  # No face
            focus_detected = False
            if arduino:
                arduino.write(b"0")  # Send '0' to Arduino

        # Optional: show webcam window for debugging
        cv2.imshow("Webcam - Press Q to quit", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def update_progress():
    global progress_value
    if focus_detected:
        progress_value += 1
        label_status.config(text="Status: Focused ✅")
    else:
        label_status.config(text="Status: Distracted ❌")

    # Limit and update
    if progress_value > progress_max:
        progress_value = progress_max
    progress["value"] = progress_value

    root.after(100, update_progress)  # run again every 100ms

# ---------- Start Threads ----------
threading.Thread(target=detect_face, daemon=True).start()
update_progress()

# ---------- Run GUI ----------
root.mainloop()

# Close serial on exit
if arduino:
    arduino.close()
