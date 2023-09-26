import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
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

    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        landmarks = results.pose_landmarks.landmark
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
        right_thumb = landmarks[mp_pose.PoseLandmark.RIGHT_THUMB]
        right_index = landmarks[mp_pose.PoseLandmark.RIGHT_INDEX]
        
        print(right_thumb.y > right_index.y)
        if right_shoulder.y < 0.15:
            if not is_jumping:
                is_jumping = True
                jump_count += 1
        else:
            is_jumping = False

    cv2.putText(frame, f"Jump Count: {jump_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Jump Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

