import os
import cv2
import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense, Input

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define and load the emotion detection model
emotion_model = Sequential([
    Input(shape=(48, 48, 1)),
    Conv2D(32, kernel_size=(3, 3), activation='relu'),
    Conv2D(64, kernel_size=(3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.25),
    Conv2D(128, kernel_size=(3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(128, kernel_size=(3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.25),
    Flatten(),
    Dense(1024, activation='relu'),
    Dropout(0.5),
    Dense(7, activation='softmax')
])
emotion_model.load_weights(os.path.join(BASE_DIR, 'model.h5'))

# Load face cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Emotion labels
emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

class VideoCamera:
    """Handles video streaming and emotion detection."""
    
    def __init__(self):
        self.stream = cv2.VideoCapture(0)
        if not self.stream.isOpened():
            raise RuntimeError("Could not access the webcam.")
    
    def __del__(self):
        self.stream.release()

    def get_frame(self):
        """Captures a frame and predicts emotion."""
        ret, frame = self.stream.read()
        if not ret:
            return None, 4  # Default to Neutral if no frame is captured

        # Convert the frame to grayscale for face detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        # Default emotion is Neutral
        emotion_code = 4

        for (x, y, w, h) in faces:
            # Extract the face ROI
            roi_gray = gray_frame[y:y + h, x:x + w]
            roi_gray = cv2.resize(roi_gray, (48, 48))
            roi_gray = roi_gray.reshape(1, 48, 48, 1).astype('float32') / 255.0  # Normalize input

            # Predict emotion
            predictions = emotion_model.predict(roi_gray)
            emotion_code = int(np.argmax(predictions))

            # Draw a rectangle around the face and label it with the detected emotion
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, emotion_dict[emotion_code], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Encode the frame to JPEG format for streaming
        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes(), emotion_code
