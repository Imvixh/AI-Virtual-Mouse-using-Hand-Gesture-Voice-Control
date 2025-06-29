import cv2
import threading
import pygetwindow as gw    
import pyautogui               
import time               

from hand_gesture import HandGesture
import voice_command 


time.sleep(1) 
try:
    active_window = gw.getActiveWindow()
    if active_window:
        active_window.minimize()
        print(f"Minimized window: {active_window.title}")
except Exception as e:
    print(f"[!] Window minimize error: {e}")


pyautogui.hotkey('win', 'd')


hand_control = HandGesture()


voice_thread = threading.Thread(target=voice_command.listen_and_execute, daemon=True)
voice_thread.start()


cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)


    frame = hand_control.control(frame)

    # Display
    # cv2.namedWindow("JARVIS - Left Hand Cursor + Right Hand Control + Voice", cv2.WINDOW_NORMAL)
    # cv2.resizeWindow("JARVIS - Left Hand Cursor + Right Hand Control + Voice", 1280, 720)

    cv2.imshow("JARVIS - Left Hand Cursor + Right Hand Control + Voice", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
