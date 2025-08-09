import cv2
import tkinter as tk
from tkinter import ttk
import threading
import serial
import time
import subprocess
import psutil
import traceback

# === CONFIG ===
COM_PORT = 'COM9'
BAUDRATE = 9600
BLINK_FRAMES_THRESHOLD = 5
BLINK_COOLDOWN = 1.0
DISTRACTION_LIMIT = 5

# === Arduino connect ===
try:
    arduino = serial.Serial(COM_PORT, BAUDRATE, timeout=1)
    time.sleep(2)
    print(f"✅ Arduino connected on {COM_PORT}")
except Exception as e:
    arduino = None
    print(f"⚠️ Arduino not connected: {e}")

# === Globals ===
progress_value = 0
progress_max = 100
focus_detected = False
dark_detected = False
blink_detected = False
blink_frame_count = 0
last_blink_time = 0
last_sent_state = None
distraction_count = 0
is_currently_distracted = False
is_monitoring_active = True

# === Tkinter GUI ===
root = tk.Tk()
root.title("Focus Loader")
root.geometry("420x160")
label_status = tk.Label(root, text="Status: Waiting...", font=("Arial", 13))
label_status.pack(pady=8)
progress = ttk.Progressbar(root, orient="horizontal", length=350, mode="determinate")
progress.pack(pady=6)

# === Haar cascades & Other Functions ===
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

def read_arduino():
    global dark_detected
    while True:
        if arduino:
            try:
                line = arduino.readline().decode(errors='ignore').strip()
                if line == "DARK": dark_detected = True
                elif line == "LIGHT": dark_detected = False
            except: pass
        time.sleep(0.05)

def check_for_browser_process():
    browser_processes = ["chrome.exe", "firefox.exe", "msedge.exe", "brave.exe"]
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] in browser_processes: return True
    return False

def update_progress():
    global progress_value, blink_detected, distraction_count, is_currently_distracted, is_monitoring_active
    if is_monitoring_active:
        if distraction_count >= DISTRACTION_LIMIT:
            print(f"Distraction limit of {DISTRACTION_LIMIT} reached. Executing test.bat...")
            try:
                # Use your correct absolute path
                subprocess.Popen(r"C:\Users\ASUS\code\uop\Face-loader\test.bat", shell=True)
            except Exception as e:
                print(f"Error executing test.bat: {e}")
            distraction_count = 0
            is_monitoring_active = False
            label_status.config(text="Paused. Waiting for browser... ⏸️")
        elif blink_detected:
            progress_value = 0; label_status.config(text="Blink detected! Resetting... 👀"); blink_detected = False
        elif dark_detected:
            progress_value = 0; label_status.config(text="Lights OFF! Restarting loader 🌑")
        elif focus_detected:
            progress_value += 1; is_currently_distracted = False; label_status.config(text=f"Focused ✅ (Distractions: {distraction_count}/{DISTRACTION_LIMIT})")
        else: # Distracted
            progress_value -= 2
            if not is_currently_distracted:
                is_currently_distracted = True; distraction_count += 1; print(f"Distraction event registered. Count is now: {distraction_count}")
            label_status.config(text=f"Distracted ❌ (Count: {distraction_count}/{DISTRACTION_LIMIT})")
    else: # Paused mode
        if check_for_browser_process():
            print("Browser detected! Resuming focus monitoring. ▶️"); is_monitoring_active = True
        else:
            progress_value = 0
    progress_value = max(0, min(progress_max, progress_value))
    progress["value"] = progress_value
    root.after(100, update_progress)

# === Face + Blink detection thread (Final Version) ===
def detect_loop():
    global focus_detected, blink_detected, blink_frame_count, last_blink_time, last_sent_state
    cap = None
    while True:
        try:
            if is_monitoring_active:
                if cap is None or not cap.isOpened():
                    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                    if not cap.isOpened():
                        print("⚠️ Cannot open camera"); time.sleep(1); continue
                ret, frame = cap.read()
                if not ret: continue
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                focus_detected = len(faces) > 0
                
                # We send the LED signal here, after detection
                if arduino:
                    # Sends '1' for distraction, '0' for focus
                    state = b'0' if focus_detected else b'1'
                    if state != last_sent_state:
                        arduino.write(state)
                        last_sent_state = state
                
                eyes_found_in_frame = False
                for (x, y, w, h) in faces:
                    roi_gray = gray[y:y+h, x:x+w]
                    eyes = eye_cascade.detectMultiScale(roi_gray)
                    if len(eyes) > 0: eyes_found_in_frame = True
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    for (ex, ey, ew, eh) in eyes: cv2.rectangle(roi_gray, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
                
                if focus_detected and not eyes_found_in_frame:
                    blink_frame_count += 1
                else:
                    blink_frame_count = 0
                    
                if blink_frame_count > BLINK_FRAMES_THRESHOLD:
                    now = time.time()
                    if now - last_blink_time > BLINK_COOLDOWN:
                        blink_detected = True; last_blink_time = now; blink_frame_count = 0
                
                # --- RE-ENABLED CAMERA WINDOW ---
                cv2.imshow("Face & Blink Detection", frame)
            else: # Paused
                if cap is not None and cap.isOpened():
                    print("Monitoring paused. Releasing camera.")
                    cap.release()
                    cv2.destroyAllWindows() # --- RE-ENABLED ---
                focus_detected = False
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except Exception as e:
            print(f"A critical error occurred! Logging to crash_log.txt")
            with open("crash_log.txt", "w") as f: traceback.print_exc(file=f)
            break
            
    if cap is not None: cap.release()
    cv2.destroyAllWindows() # --- RE-ENABLED ---
    root.quit()

# === Start threads ===
threading.Thread(target=detect_loop, daemon=True).start()
update_progress()
root.mainloop()

if arduino: arduino.close()