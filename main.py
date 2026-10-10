import cv2
import mediapipe as mp
import pyautogui
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
last_action = 0
COOLDOWN = 1.0  # seconds, prevents repeated triggers

def fingers_up(lm):
    tips = [8, 12, 16, 20]
    states = [1 if lm[t].y < lm[t-2].y else 0 for t in tips]
    thumb = 1 if lm[4].x < lm[3].x else 0   # adjust for handedness
    return [thumb] + states

while True:
    ok, frame = cap.read()
    if not ok:
        break
    frame = cv2.flip(frame, 1)
    result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if result.multi_hand_landmarks:
        lm = result.multi_hand_landmarks[0].landmark
        f = fingers_up(lm)
        now = time.time()

        if now - last_action > COOLDOWN:
            if f == [0, 1, 0, 0, 0]:        # index only
                pyautogui.press('right'); last_action = now
            elif f == [0, 1, 1, 0, 0]:      # two fingers
                pyautogui.press('left');  last_action = now
            elif f == [1, 1, 1, 1, 1]:      # open palm
                pyautogui.press('volumemute'); last_action = now

        mp_draw.draw_landmarks(frame, result.multi_hand_landmarks[0],
                               mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Gesture Control", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()