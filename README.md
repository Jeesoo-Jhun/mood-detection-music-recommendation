<iframe src="https://drive.google.com/file/d/1cX16bh_Xsq135010AdT9xfAyRXpWezW_/preview" width="640" height="480" allow="autoplay"></iframe>

# Emotion-Based Music Recommendation System

This project is an **Emotion-Based Music Recommendation System** that uses real-time webcam-based emotion detection to recommend songs that match the user's mood. It integrates a machine learning model for facial expression recognition with the Spotify API to dynamically fetch mood-specific playlists. The web application is developed using Flask.

![Emotion Detection Interface](https://cdn.smclk.net/img/Emotion-Detection.png)

## Dataset

* [Dataset Link](https://drive.google.com/drive/folders/1lvAYBLcsVehisuecNmENKVmISBkPoQyL?usp=sharing)

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Technical Details](#technical-details)
  - [Emotion Detection](#emotion-detection)
  - [Music Recommendation](#music-recommendation)
  - [Web Interface](#web-interface)
- [Folder Structure](#folder-structure)
- [Future Enhancements](#future-enhancements)
- [Acknowledgments](#acknowledgments)

## Overview
The Emotion-Based Music Recommendation System leverages computer vision to analyze a user’s facial expressions and predict their current emotional state. Based on the detected emotion, it recommends songs curated from Spotify or local backups. The web app combines state-of-the-art machine learning with intuitive design to provide a seamless user experience.

## Features
- **Real-Time Emotion Detection**: Captures facial expressions using a webcam and predicts emotions like Happy, Sad, Angry, etc.
- **Dynamic Music Recommendation**: Suggests Spotify playlists or local backup songs based on the detected emotion.
- **Responsive Web Interface**: Provides a clean and user-friendly interface for interacting with the system.

## Setup Instructions

### Prerequisites
1. Python 3.7 or later
2. Virtual Environment (recommended)
3. Spotify Developer Account for API credentials

### Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/emotion-music-recommendation.git
   cd emotion-music-recommendation
   ```

2. **Create a Virtual Environment**:
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate  # For Windows: myenv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Spotify API**:
   - Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
   - Create a new app and obtain the `Client ID` and `Client Secret`.
   - Update the `CLIENT_ID` and `CLIENT_SECRET` in the `Spotipy.py` file.

5. **Download Pretrained Model**:
   Place the `model.h5` file in the root directory. Ensure the model aligns with the expected input shape (48x48 grayscale).

6. **Run the Application**:
   ```bash
   python app.py
   ```
   Access the app at `http://127.0.0.1:5000` in your browser.

## Usage
- Allow webcam access when prompted by your browser.
- The app detects your facial expression and displays the predicted emotion.
- A curated playlist based on the detected emotion will be displayed in the table.
- Press `q` to quit the application if testing locally.

## Technical Details

### Emotion Detection
- **Model**: Convolutional Neural Network (CNN) trained on the FER2013 dataset.
- **Input**: 48x48 grayscale image.
- **Output**: One of seven emotions - Happy, Sad, Angry, Neutral, Disgusted, Fearful, Surprised.
- **Tool**: OpenCV is used for face detection.

### Music Recommendation
- **Spotify Integration**: Fetches playlists dynamically using the Spotify Web API.
- **Local Backup**: If the Spotify API fails, the app fetches songs from preloaded CSV files.
- **Mapping**: Each emotion is mapped to a unique playlist ID.

### Web Interface
- **Framework**: Flask for backend, Jinja2 for templating.
- **Design**: Bootstrap for a responsive and visually appealing layout.
- **Refresh**: The app updates song recommendations every 5 seconds based on detected emotion.

## Folder Structure
```
.
├── app.py                 # Main Flask application
├── camera.py              # Video capture and emotion detection logic
├── Spotipy.py             # Spotify API integration and music recommendation logic
├── templates/
│   └── index.html         # Web interface template
├── static/
│   ├── css/
│   │   └── style.css      # Custom stylesheets
├── model.h5               # Pretrained emotion detection model
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## Future Enhancements
- **Multiple Emotion Detection**: Support detecting multiple faces and emotions simultaneously.
- **Real-Time Audio Playback**: Automatically play recommended songs within the app.
- **Advanced Models**: Use a more robust model for better emotion recognition accuracy.
- **Mobile Compatibility**: Optimize for mobile devices.

## Acknowledgments
- [FER2013 Dataset](https://www.kaggle.com/c/challenges-in-representation-learning-facial-expression-recognition-challenge) for training the emotion model.
- [Spotify Developer API](https://developer.spotify.com/) for enabling playlist integration.
- Flask and Bootstrap for web application development.
