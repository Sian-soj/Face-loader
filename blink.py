import cv2
import tkinter as tk
from tkinter import ttk
import threading
import serial
import time

# --- Connect to Arduino ---
try:
    arduino = serial.Serial('COM9', 9600, timeout=1)  # Change COM port if needed
    time.sleep(2)
    print("✅ Arduino connected on COM9")
except:
    arduino = None
    print("⚠️ Arduino not connected — simulation mode")

# --- Haar cascades ---
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

cap = cv2.VideoCapture(0)

# --- GUI setup ---
root = tk.Tk()
root.title("Focus Loader with Blink + Darkness Reset")
root.geometry("400x150")

label_status = tk.Label(root, text="Status: Waiting...", font=("Arial", 14))
label_status.pack(pady=10)

progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress.pack(pady=10)

progress_value = 0
progress_max = 100
focus_detected = False
blink_detected = False
blink_timer = 0
dark_detected = False
blink_threshold_frames = 5

# --- Thread: LDR reading from Arduino ---
def check_light_sensor():
    global dark_detected
    while True:
        if arduino:
            try:
                data = arduino.readline().decode().strip()
                if data == "DARK":
                    dark_detected = True
                elif data == "LIGHT":
                    dark_detected = False
            except:
                pass
        time.sleep(0.1)

# --- Thread: Face & Eye detection ---
def detect_face_and_eyes():
    global focus_detected, blink_detected, blink_timer

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        focus_detected = len(faces) > 0

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

            eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 4)

            if len(eyes) == 0:
                blink_timer += 1
            else:
                blink_timer = 0

            blink_detected = blink_timer >= blink_threshold_frames

            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

        # Send LED control to Arduino
        if arduino:
            try:
                if focus_detected:
                    arduino.write(b'1')  # Focused → LED OFF
                else:
                    arduino.write(b'0')  # Distracted → LED ON
            except:
                pass

        cv2.imshow("Eye Tracker - Press Q to quit", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# --- Progress bar updater ---
def update_progress():
    global progress_value

    if blink_detected:
        progress_value = 0
        label_status.config(text="Blink detected! Resetting... 👀❌")
    elif dark_detected:
        progress_value = 0
        label_status.config(text="Lights OFF! Restarting loader 🌑")
    elif focus_detected:
        progress_value += 1
        label_status.config(text="Focused ✅")
    else:
        progress_value -= 2
        label_status.config(text="Distracted ❌")

    progress_value = max(0, min(progress_max, progress_value))
    progress["value"] = progress_value

    root.after(100, update_progress)

# --- Start threads ---
threading.Thread(target=detect_face_and_eyes, daemon=True).start()
threading.Thread(target=check_light_sensor, daemon=True).start()
update_progress()
root.mainloop()

if arduino:
    arduino.close()
