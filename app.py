from flask import Flask, render_template, Response
from camera import VideoCamera, VideoFileCamera
from Spotipy import music_rec
import os

app = Flask(__name__)

headings = ("Name", "Album", "Artist")

# Check if running on Render (no webcam support)
IS_RENDER_ENV = os.environ.get("RENDER", False)

# Use webcam for local testing, else use video file
camera = VideoCamera() if not IS_RENDER_ENV else VideoFileCamera()

current_emotion = 4  # Default to Neutral

@app.route('/')
def index():
    global current_emotion
    _, emotion_code = camera.get_frame()
    if emotion_code != current_emotion:  # Update only if emotion changes
        current_emotion = emotion_code
    df = music_rec(current_emotion)
    return render_template('index.html', headings=headings, data=df.to_dict(orient="records"))

def gen(camera):
    """Video feed generator."""
    global current_emotion
    while True:
        frame, emotion_code = camera.get_frame()
        if emotion_code != current_emotion:  # Update emotion
            current_emotion = emotion_code
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
