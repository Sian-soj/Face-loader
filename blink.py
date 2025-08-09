import cv2
import tkinter as tk
from tkinter import ttk
import threading
import serial
import time
import subprocess # <-- ADDED: To run external commands/files

# === CONFIG ===
COM_PORT = 'COM9'      # change if needed
BAUDRATE = 9600
BLINK_FRAMES_THRESHOLD = 5   # how many consecutive frames with no eyes = blink
BLINK_COOLDOWN = 1.0         # seconds before another blink is registered
DISTRACTION_LIMIT = 5        # <-- ADDED: How many distractions before action

# === Arduino connect ===
try:
    arduino = serial.Serial(COM_PORT, BAUDRATE, timeout=1)
    time.sleep(2)
    print(f"✅ Arduino connected on {COM_PORT}")
except Exception as e:
    arduino = None
    print("⚠️ Arduino not connected:", e)

# === Globals ===
progress_value = 0
progress_max = 100
focus_detected = False
dark_detected = False
blink_detected = False
blink_frame_count = 0
last_blink_time = 0
last_sent_state = None
distraction_count = 0         # <-- ADDED: The distraction counter
is_currently_distracted = False # <-- ADDED: A state flag for counting accurately

# === Tkinter GUI ===
root = tk.Tk()
root.title("Focus Loader (Haar cascade blink detection)")
root.geometry("420x160")

label_status = tk.Label(root, text="Status: Waiting...", font=("Arial", 13))
label_status.pack(pady=8)

progress = ttk.Progressbar(root, orient="horizontal", length=350, mode="determinate")
progress.pack(pady=6)

# === Haar cascades ===
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

# === Arduino LDR reader thread ===
def read_arduino():
    global dark_detected
    while True:
        if arduino:
            try:
                line = arduino.readline().decode(errors='ignore').strip()
                if line == "DARK":
                    dark_detected = True
                elif line == "LIGHT":
                    dark_detected = False
            except:
                pass
        time.sleep(0.05)

# === Face + Blink detection thread ===
def detect_loop():
    # ... (This function remains exactly the same as before) ...
    global focus_detected, blink_detected, blink_frame_count, last_blink_time, last_sent_state

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("⚠️ Cannot open camera")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        focus_detected = len(faces) > 0
        eyes_found_in_frame = False

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)

            if len(eyes) > 0:
                eyes_found_in_frame = True

            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_gray, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
        
        if focus_detected and not eyes_found_in_frame:
            blink_frame_count += 1
        else:
            blink_frame_count = 0
            
        if blink_frame_count > BLINK_FRAMES_THRESHOLD:
            now = time.time()
            if now - last_blink_time > BLINK_COOLDOWN:
                blink_detected = True
                last_blink_time = now
                blink_frame_count = 0

        if arduino:
            try:
                state = b'1' if focus_detected else b'0'
                if state != last_sent_state:
                    arduino.write(state)
                    last_sent_state = state
            except:
                pass

        cv2.imshow("Face & Blink Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    root.quit()

# === Progress updater ===
def update_progress():
    global progress_value, blink_detected, distraction_count, is_currently_distracted # <-- MODIFIED

    # Check for distraction limit first
    if distraction_count >= DISTRACTION_LIMIT:
        label_status.config(text=f"Limit reached! Closing Chrome...")
        print(f"Distraction limit of {DISTRACTION_LIMIT} reached. Executing test.bat...")
        try:
            # Run the batch file. shell=True is needed for .bat files on Windows.
            subprocess.run(r"C:\Users\ASUS\code\uop\Face-loader\test.bat", shell=True, check=True)
            print("test.bat executed successfully.")
        except FileNotFoundError:
            print("ERROR: 'test.bat' not found. Make sure it's in the same folder as the script.")
        except subprocess.CalledProcessError:
            print("ERROR: 'test.bat' failed to execute correctly.")
        
        root.quit() # Close this application
        return # Stop the update loop

    if blink_detected:
        progress_value = 0
        label_status.config(text="Blink detected! Resetting... 👀")
        blink_detected = False
    elif dark_detected:
        progress_value = 0
        label_status.config(text="Lights OFF! Restarting loader 🌑")
    elif focus_detected:
        progress_value += 1
        # If the user was distracted, this marks their return to focus.
        is_currently_distracted = False
        label_status.config(text=f"Focused ✅ (Distractions: {distraction_count}/{DISTRACTION_LIMIT})")
    else: # Distracted
        progress_value -= 2
        # This logic ensures we only count each distraction *once*.
        if not is_currently_distracted:
            is_currently_distracted = True
            distraction_count += 1
            print(f"Distraction event registered. Count is now: {distraction_count}")
        label_status.config(text=f"Distracted ❌ (Count: {distraction_count}/{DISTRACTION_LIMIT})")

    progress_value = max(0, min(progress_max, progress_value))
    progress["value"] = progress_value

    root.after(100, update_progress)

# === Start threads ===
threading.Thread(target=detect_loop, daemon=True).start()
threading.Thread(target=read_arduino, daemon=True).start()
update_progress()
root.mainloop()

if arduino:
    arduino.close()