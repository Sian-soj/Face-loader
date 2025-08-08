import cv2
import tkinter as tk
from tkinter import ttk
import threading
import serial
import time

# --- Try to connect to Arduino ---
try:
    arduino = serial.Serial('COM9', 9600, timeout=1)
    time.sleep(2)
    print("✅ Arduino connected on COM9")
except:
    arduino = None
    print("⚠️ Arduino not connected — running in simulation mode")

# --- Face detection setup ---
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)

# --- GUI Setup ---
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

# --- Face detection thread ---
def detect_face():
    global focus_detected

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Failed to grab frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        focus_detected = len(faces) > 0

        # Send signal to Arduino
        if arduino:
            try:
                arduino.write(b'1' if focus_detected else b'0')
            except:
                print("⚠️ Failed to write to Arduino.")

        # Show webcam window
        cv2.imshow("Webcam - Press Q to quit", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# --- Progress Bar Update ---
def update_progress():
    global progress_value

    if focus_detected:
        progress_value += 1
        label_status.config(text="Status: Focused ✅")
    else:
        progress_value -= 2
        label_status.config(text="Status: Distracted ❌")

    progress_value = max(0, min(progress_max, progress_value))
    progress["value"] = progress_value

    root.after(100, update_progress)

# --- Start everything ---
threading.Thread(target=detect_face, daemon=True).start()
update_progress()
root.mainloop()

# --- Cleanup ---
if arduino:
    arduino.close()
