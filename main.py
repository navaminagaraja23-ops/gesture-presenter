import cv2
import time
import pyautogui
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

COOLDOWN = 1.0
LOCK_HOLD = 1.5

# gesture: (key, command, seconds to hold)
ACTIONS = {
    "index": ("right", "Next slide", 0.4),
    "two": ("left", "Previous slide", 0.4),
    "three": ("b", "Black screen on/off", 0.6),
    "pinky": ("esc", "End slideshow", 0.8),
    "thumb": ("home", "First slide", 0.6),
    "palm": ("volumemute", "Mute / unmute", 1.0),
}

def fingers_up(lm):
    return tuple(1 if lm[t].y < lm[t - 2].y else 0
                 for t in (8, 12, 16, 20))

def thumb_up(lm):
    top = min(lm[6].y, lm[10].y, lm[14].y, lm[18].y)
    return lm[4].y < top - 0.05

def classify(lm):
    f = fingers_up(lm)
    if f == (0, 0, 0, 0):
        return "thumb" if thumb_up(lm) else "fist"
    if f == (1, 0, 0, 0): return "index"
    if f == (1, 1, 0, 0): return "two"
    if f == (1, 1, 1, 0): return "three"
    if f == (0, 0, 0, 1): return "pinky"
    if f == (1, 1, 1, 1): return "palm"
    return None

cap = cv2.VideoCapture(0)
armed = False
last_gesture = None
hold_start = time.time()
last_action = 0
done = False
message = ""

while True:
    ok, frame = cap.read()
    if not ok:
        break
    frame = cv2.flip(frame, 1)
    result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    gesture = None
    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        gesture = classify(hand.landmark)
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

    now = time.time()
    if gesture != last_gesture:
        last_gesture = gesture
        hold_start = now
        done = False
    held = now - hold_start

    if gesture and not done:
        if gesture == "fist" and held > LOCK_HOLD:
            armed = not armed
            done = True
            message = "UNLOCKED" if armed else "LOCKED"
        elif armed and gesture in ACTIONS:
            key, label, need = ACTIONS[gesture]
            if held >= need and now - last_action > COOLDOWN:
                pyautogui.press(key)
                last_action = now
                done = True
                message = label

    status = "ARMED" if armed else "LOCKED - hold fist 1.5s"
    color = (0, 255, 0) if armed else (0, 0, 255)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, status, (10, 30), font, 0.8, color, 2)
    cv2.putText(frame, "Seeing: " + str(gesture), (10, 65),
                font, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, message, (10, 100), font, 0.8, (255, 255, 0), 2)
    cv2.imshow("Gesture Control", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()