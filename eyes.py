import cv2
import numpy as np
from ultralytics import YOLO
#import ultralytics
import pyttsx3
import threading
import time

# Colors for bounding boxes
COLORS = np.random.uniform(0, 255, size=(80, 3))

# Load YOLO model
model = YOLO('yolov8n.pt')

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Dictionary to store the last announced state for each object
object_states = {}

# Default distance threshold and known width (for all objects)
DEFAULT_DISTANCE_THRESHOLD = 3.0
DEFAULT_KNOWN_WIDTH = 0.5  # Default width for unknown objects (in meters)

# Camera parameters (you need to calibrate these for your specific camera)
FOCAL_LENGTH = 1000  # in pixels

def calculate_distance(width_in_pixels, real_width):
    return (real_width * FOCAL_LENGTH) / width_in_pixels

def get_direction(x, img_width):
    center = img_width / 2
    if x < center - img_width / 6:
        return "left"
    elif x > center + img_width / 6:
        return "right"
    else:
        return "in front"

def speak(text):
    threading.Thread(target=engine.say, args=(text,)).start()
    engine.runAndWait()

def should_announce(object_id, distance, direction):
    current_time = time.time()
    if object_id not in object_states:
        object_states[object_id] = {
            "last_distance": distance,
            "last_direction": direction,
            "last_announcement": current_time
        }
        return True
    
    last_state = object_states[object_id]
    time_since_last_announcement = current_time - last_state["last_announcement"]
    distance_change = abs(distance - last_state["last_distance"]) / last_state["last_distance"] if last_state["last_distance"] > 0 else 0
    direction_changed = direction != last_state["last_direction"]
    
    if (distance_change > 0.1 or direction_changed) and time_since_last_announcement > 5:
        object_states[object_id] = {
            "last_distance": distance,
            "last_direction": direction,
            "last_announcement": current_time
        }
        return True
    
    return False

cap = cv2.VideoCapture(0)
last_detection_time = time.time()

print("Press 'q' to quit the program.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame. Exiting...")
        break

    current_time = time.time()
    if current_time - last_detection_time >= 10:
        height, width = frame.shape[:2]
        results = model(frame)

        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls = int(box.cls[0])
                obj_type = model.names[cls]

                # Calculate the width of the bounding box and distance
                obj_width = x2 - x1
                distance = calculate_distance(obj_width, DEFAULT_KNOWN_WIDTH)

                # Set a default distance threshold for all objects
                if distance <= DEFAULT_DISTANCE_THRESHOLD:
                    direction = get_direction((x1 + x2) / 2, width)
                    object_id = f"{obj_type}{x1}{y1}"

                    if should_announce(object_id, distance, direction):
                        speak_text = f"{obj_type} detected at {distance:.1f} meters {direction}"
                        speak(speak_text)

                    color = tuple(map(int, COLORS[cls % len(COLORS)]))
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    label = f"{obj_type.capitalize()}: {distance:.2f} m, {direction}"
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        cv2.imshow("YOLO Detection with Distance and Direction", frame)
        last_detection_time = current_time

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        print("'q' pressed. Terminating the program...")
        break

cap.release()
cv2.destroyAllWindows()
print("Program terminated.")





