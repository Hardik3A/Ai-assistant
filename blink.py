import cv2
import mediapipe as mp
import pyautogui

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

def eye_aspect_ratio(landmarks, eye_indices):
    # Calculate the vertical eye distances
    v1 = landmarks[eye_indices[1]].y - landmarks[eye_indices[5]].y
    v2 = landmarks[eye_indices[2]].y - landmarks[eye_indices[4]].y
    # Calculate the horizontal eye distance
    h = landmarks[eye_indices[0]].x - landmarks[eye_indices[3]].x
    # Calculate the eye aspect ratio
    ear = (v1 + v2) / (2.0 * h)
    return ear

# Define indices for left and right eyes
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

# Threshold for detecting a blink
BLINK_THRESHOLD = 0.2

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape
    if landmark_points:
        landmarks = landmark_points[0].landmark
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))
            if id == 1:
                screen_x = screen_w * landmark.x
                screen_y = screen_h * landmark.y
                pyautogui.moveTo(screen_x, screen_y)
        
        # Calculate eye aspect ratios
        left_ear = eye_aspect_ratio(landmarks, LEFT_EYE)
        right_ear = eye_aspect_ratio(landmarks, RIGHT_EYE)
        
        # Detect left eye blink
        if left_ear < BLINK_THRESHOLD:
            pyautogui.click(button='left')
            pyautogui.sleep(0.5)  # Delay to prevent multiple clicks
        
        # Detect right eye blink
        if right_ear < BLINK_THRESHOLD:
            pyautogui.click(button='right')
            pyautogui.sleep(0.5)  # Delay to prevent multiple clicks
        
        # Visualize eye landmarks
        for eye in [LEFT_EYE, RIGHT_EYE]:
            for i in eye:
                x = int(landmarks[i].x * frame_w)
                y = int(landmarks[i].y * frame_h)
                cv2.circle(frame, (x, y), 2, (0, 255, 255), -1)
    
    cv2.imshow('Eye Controlled Mouse', frame)
    
    # Check for 'Q' key press to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cam.release()
cv2.destroyAllWindows()