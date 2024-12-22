from flask import Flask, render_template, Response
from camera import VideoCamera
from Spotipy import music_rec

app = Flask(__name__)

headings = ("Name", "Album", "Artist")
camera = VideoCamera()
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
    app.run(debug=True)
