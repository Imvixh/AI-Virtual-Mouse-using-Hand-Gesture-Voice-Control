import cv2
import mediapipe as mp
import pyautogui
import os
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

class HandGesture:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.4)
        self.mp_draw = mp.solutions.drawing_utils
        self.finger_tips_ids = [4, 8, 12, 16, 20]

        self.screen_w, self.screen_h = pyautogui.size()
        self.prev_right_click = False
        self.pinch_hold_frames = 0
        self.prev_x = 0
        self.prev_y = 0

        
        self.last_click_time = 0
        self.double_click_delay = 3 # seconds

    def control(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                label = handedness.classification[0].label
                lm_list = []
                h, w, _ = frame.shape

                for id, lm in enumerate(hand_landmarks.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append((id, cx, cy))

                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                fingers = []
                fingers.append(1 if lm_list[4][1] > lm_list[3][1] else 0)
                for id in range(1, 5):
                    fingers.append(1 if lm_list[self.finger_tips_ids[id]][2] < lm_list[self.finger_tips_ids[id] - 2][2] else 0)

                total_fingers = fingers.count(1)

                if label == "Left":
                    
                    mid_x, mid_y = lm_list[12][1], lm_list[12][2]
                    margin = 100
                    min_x, max_x = margin, w - margin
                    min_y, max_y = margin, h - margin

                    mid_x = np.clip(mid_x, min_x, max_x)
                    mid_y = np.clip(mid_y, min_y, max_y)
                    screen_x = int(np.interp(mid_x, [min_x, max_x], [0, self.screen_w]))
                    screen_y = int(np.interp(mid_y, [min_y, max_y], [0, self.screen_h]))

                    jitter_threshold = 7
                    dx = abs(screen_x - self.prev_x)
                    dy = abs(screen_y - self.prev_y)
                    if dx > jitter_threshold or dy > jitter_threshold:
                        smooth_factor = 0.5
                        self.prev_x += (screen_x - self.prev_x) * smooth_factor
                        self.prev_y += (screen_y - self.prev_y) * smooth_factor
                        pyautogui.moveTo(int(self.prev_x), int(self.prev_y))

                    # Pinch = click logic
                    thumb_x, thumb_y = lm_list[4][1], lm_list[4][2]
                    index_x, index_y = lm_list[8][1], lm_list[8][2]
                    distance = ((thumb_x - index_x) ** 2 + (thumb_y - index_y) ** 2) ** 0.5

                    pinch_threshold = 30
                    click_hold_threshold = 10

                    if distance < pinch_threshold:
                        self.pinch_hold_frames += 1

                        if self.pinch_hold_frames == 3:
                            import time
                            current_time = time.time()
                            time_diff = current_time - self.last_click_time

                            if time_diff < self.double_click_delay:
                                pyautogui.doubleClick()
                                self.last_click_time = 0
                                cv2.putText(frame, 'Left: Double Click', (50, 50),
                                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
                            else:
                                pyautogui.mouseDown()
                                self.last_click_time = current_time

                        if self.pinch_hold_frames > click_hold_threshold:
                            cv2.putText(frame, 'Left: Holding...', (50, 50),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

                    else:
                        if self.pinch_hold_frames > 0:
                            if self.pinch_hold_frames < click_hold_threshold:
                                pyautogui.click()
                                cv2.putText(frame, 'Left: Single Click', (50, 50),
                                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                            else:
                                pyautogui.mouseUp()
                        self.pinch_hold_frames = 0

                elif label == "Right":
                    if total_fingers == 2 and fingers[1] and fingers[2]:
                        pyautogui.scroll(-140)
                        cv2.putText(frame, 'Right: Scroll Down', (50, 100),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    elif total_fingers == 3 and fingers[1] and fingers[2] and fingers[3]:
                        pyautogui.scroll(100)
                        cv2.putText(frame, 'Right: Scroll Up', (50, 100),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    if total_fingers == 4:
                        if not self.prev_right_click:
                            pyautogui.rightClick()
                            self.prev_right_click = True
                        cv2.putText(frame, 'Right: Right Click', (50, 150),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    else:
                        self.prev_right_click = False

        return frame
