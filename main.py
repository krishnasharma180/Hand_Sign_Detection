import cv2
import mediapipe as mp
import pyttsx3

# MediaPipe Hands

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.9)

prediction_count = 0
threshold_count = 7  


# OpenCV Video Capture
cap = cv2.VideoCapture(0)

last_gesture = None
spoken_gesture=None


# gesture detection function

def detect_gesture(landmarks):
    fingers = []
    tip_ids = [4, 8, 12, 16, 20]

    # Thumb
    if landmarks[4].x < landmarks[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other 4 fingers
    for i in range(1, 5):
        if landmarks[tip_ids[i]].y < landmarks[tip_ids[i] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    total_fingers = fingers.count(1)

    
    if total_fingers == 5:
        return "Hello"
    elif (landmarks[0].z-landmarks[9].z)>0.05:
        return "Byee"
    elif fingers==[0,1,0,0,0]:
        return "My"
    elif fingers == [1, 0, 0, 0, 0]:
        return "is"
    elif fingers==[0,1,1,0,0,]:
        return "Name"
    elif fingers==[0,1,0,0,1]:
        return "Krishna"
    elif fingers==[0,0,1,1,1] and landmarks[tip_ids[0]].y>=landmarks[tip_ids[1]].y:
        return "Ok"
    elif fingers==[1,0,0,0,1]:
        return "What"
    elif fingers==[1,1,0,0,0]:
        return "Your"
    else:
        return "Unknown"

# Speaking functionality
        
def speak(gesture):
    engine=pyttsx3.init()
    engine.say(gesture)
    engine.runAndWait()

# Camaera functionality

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            gesture = detect_gesture(hand_landmarks.landmark)
          
            if gesture == last_gesture:
                  prediction_count += 1
            else:
                  prediction_count = 0
                  

            if prediction_count >= threshold_count:
                if gesture !='Unknown' and gesture!=spoken_gesture:
                        speak(gesture)
                        spoken_gesture=gesture
                        prediction_count = 0
           
            last_gesture = gesture
            if gesture != spoken_gesture and prediction_count == 0:
                spoken_gesture = ""
            cv2.putText(frame, f"Gesture: {gesture}", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Sign to Speech", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
       

cap.release()
cv2.destroyAllWindows()
print("Camera closed.")
