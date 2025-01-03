import os
import cv2
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense, Input
import requests

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Google Drive file for the model
MODEL_FILE_ID = "18QVC9UEbDzwrPHszFCx_AxVZlk0UTExP"
MODEL_URL = f"https://drive.google.com/uc?id={MODEL_FILE_ID}&export=download"
MODEL_PATH = os.path.join(BASE_DIR, "model.h5")

# Google Drive file for video
VIDEO_FILE_ID = "1Ih2s478fe5a8k9OLfRoQz3WBQDkIt88M"
VIDEO_URL = f"https://drive.google.com/uc?id={VIDEO_FILE_ID}&export=download"
VIDEO_PATH = os.path.join(BASE_DIR, "happy_and_surprise.mp4")

def download_file(url, destination):
    """Downloads a file from a URL if it doesn't exist locally."""
    if not os.path.exists(destination):
        print(f"Downloading {os.path.basename(destination)} from Google Drive...")
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(destination, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"{os.path.basename(destination)} downloaded successfully.")
        else:
            print(f"Failed to download {os.path.basename(destination)}. Status code: {response.status_code}")
            exit(1)

# Ensure the model and video are downloaded
download_file(MODEL_URL, MODEL_PATH)
download_file(VIDEO_URL, VIDEO_PATH)

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
emotion_model.load_weights(MODEL_PATH)

# Load face cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Emotion labels
emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

class VideoCamera:
    """Handles webcam video streaming and emotion detection."""
    def __init__(self):
        self.stream = cv2.VideoCapture(0)
        if not self.stream.isOpened():
            raise RuntimeError("Could not access the webcam.")

    def __del__(self):
        self.stream.release()

    def get_frame(self):
        ret, frame = self.stream.read()
        if not ret:
            return None, 4  # Default to Neutral if no frame is captured

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        emotion_code = 4
        for (x, y, w, h) in faces:
            roi_gray = gray_frame[y:y + h, x:x + w]
            roi_gray = cv2.resize(roi_gray, (48, 48))
            roi_gray = roi_gray.reshape(1, 48, 48, 1).astype('float32') / 255.0

            predictions = emotion_model.predict(roi_gray)
            emotion_code = int(np.argmax(predictions))

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, emotion_dict[emotion_code], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes(), emotion_code

class VideoFileCamera:
    """Handles pre-recorded video streaming and emotion detection."""
    def __init__(self):
        self.stream = cv2.VideoCapture(VIDEO_PATH)
        if not self.stream.isOpened():
            raise RuntimeError("Could not access the video file.")

    def __del__(self):
        self.stream.release()

    def get_frame(self):
        ret, frame = self.stream.read()
        if not ret:
            self.stream.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop the video
            ret, frame = self.stream.read()

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        emotion_code = 4
        for (x, y, w, h) in faces:
            roi_gray = gray_frame[y:y + h, x:x + w]
            roi_gray = cv2.resize(roi_gray, (48, 48))
            roi_gray = roi_gray.reshape(1, 48, 48, 1).astype('float32') / 255.0

            predictions = emotion_model.predict(roi_gray)
            emotion_code = int(np.argmax(predictions))

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, emotion_dict[emotion_code], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes(), emotion_code
