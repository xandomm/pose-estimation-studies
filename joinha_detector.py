import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose
hands = mp_hands.Hands()
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)  

is_jumping = False
jump_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    hands_results = hands.process(rgb_frame)
    pose_results = pose.process(rgb_frame)

    if hands_results.multi_hand_landmarks:
        for landmarks in hands_results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

        right_hand_landmarks = hands_results.multi_hand_landmarks[0]
        thumb_tip = right_hand_landmarks.landmark[4]  
        index_finger_tip = right_hand_landmarks.landmark[8] 
        print(thumb_tip.y < index_finger_tip.y, thumb_tip.y, index_finger_tip.y)
        if thumb_tip.y < index_finger_tip.y + .15:
            is_jumping = True
    
    
    if is_jumping:
        phrase = f"NUMERO DE PULOS: {jump_count}"
        if pose_results.pose_landmarks:
            landmarks = pose_results.pose_landmarks.landmark
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
            if right_shoulder.y < right_wrist.y:
                if not is_jumping:
                    is_jumping = True
                    jump_count += 1
            else:
                is_jumping = False
    else:
        phrase = "FACA O JOIA IMEDIATAMENTE"


    cv2.putText(frame, phrase, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Jump Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()