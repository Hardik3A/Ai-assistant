# Ai-assistant
# Vision-Based Accessibility System  

This repository contains two independent modules that enhance computer interaction through vision-based systems:  

1. **Object Detection with Distance and Direction**  
   - Detects objects in real-time and provides spatial feedback (e.g., left, right, or in front).  

2. **Cursor Control Using Eye Tracking**  
   - Enables hands-free control of the computer cursor using eye movements and blinks.  

---

## Modules  

### 1. Object Detection with Distance and Direction  

#### Features  
- Real-time object detection using YOLOv8.  
- Distance estimation for detected objects.  
- Spatial feedback (e.g., "Object detected 2 meters to the left").  

#### How It Works  
- **YOLOv8 Model**: Identifies objects in the video feed.  
- **Bounding Boxes**: Measures object width in pixels to estimate distance.  
- **Direction Detection**: Determines if an object is to the left, right, or in front of the user.  
- **Audio Feedback**: Announces object type, distance, and direction.  

#### Run Instructions  
1. Install required libraries:  
   ```bash
   pip install -r requirements.txt
   ```  
2. Run the script:  
   ```bash
   python object_detection.py
   ```  

---

### 2. Cursor Control Using Eye Tracking  

#### Features  
- Tracks eye movements to move the cursor.  
- Detects blinks for left and right mouse clicks.  

#### How It Works  
- **Mediapipe Face Mesh**: Detects facial landmarks and calculates Eye Aspect Ratio (EAR).  
- **Gaze Tracking**: Maps eye movements to screen coordinates for cursor control.  
- **Blink Detection**: Simulates mouse clicks (left and right) based on blinks.  

#### Run Instructions  
1. Install required libraries:  
   ```bash
   pip install -r requirements.txt
   ```  
2. Run the script:  
   ```bash
   python eye_tracking_cursor.py
   ```  

---

## Installation  

1. Clone the repository:  
   ```bash
   git clone https://github.com/your-username/vision-accessibility-system.git
   cd vision-accessibility-system
   ```  

2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```  

3. Ensure a webcam is connected to your system.  

---

## Technology Stack  

- **Object Detection**:  
  - YOLOv8 for real-time object identification.  
  - OpenCV for image processing.  
  - Pyttsx3 for text-to-speech feedback.  

- **Cursor Control**:  
  - Mediapipe for facial landmark detection.  
  - PyAutoGUI for cursor control and mouse click simulation.  

---

## Use Cases  

- **Assistive Technology**:  
  - Hands-free computing for individuals with motor impairments.  
  - Enhances accessibility through visual and auditory feedback.  

- **Object Awareness**:  
  - Identifies objects in the surroundings with precise spatial guidance.  

---

## Contributing  

Contributions are welcome! Submit issues or pull requests to improve the project.  

---

