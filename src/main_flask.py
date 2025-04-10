"""
Path: src/main.py
"""

import cv2
from flask import Flask, Response


class MainApp:
    def __init__(self, logger):
        self.logger = logger
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def home():
            return "¡Hola, mundo! Esta es una página sencilla con Flask."

        @self.app.route('/video_feed')
        def video_feed():
            return Response(self.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def generate_frames(self):
        camera = cv2.VideoCapture(0)
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        camera.release()

    def run(self):
        self.logger.info("Aplicación iniciada.")
        self.app.run(debug=True)
