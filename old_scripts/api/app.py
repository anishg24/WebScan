#  Copyright (c) 2020. Anish Govind
#  https://github.com/anishg24

from collections import Counter
from flask import Flask, render_template, Response
from api.python_scripts.camera import VideoCamera
import threading

app = Flask(__name__)
lock = threading.Lock()
video_camera = VideoCamera()
current_score = None

@app.route("/stream", methods=["GET"])
def stream():
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/score", methods=["GET"])
def get_score():
    global current_score
    return {"score": current_score}

def generate():
    global video_camera
    global current_score
    scores_counter = Counter()
    if video_camera is None:
        video_camera = VideoCamera()
    while True:
        with lock:
            frame, _, score = video_camera.get_video_frame()
            if score:
                scores_counter[score] += 1
            if scores_counter and scores_counter.most_common()[0][1] >= 5:
                if score:
                    print(score)
                    current_score = score
        yield b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)
