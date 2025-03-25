"""
Path: src/routes/video_routes.py
"""

from flask import Blueprint, Response
from src.camera import Camera
from src.utils.logging.simple_logger import LoggerService
import cv2  # nuevo import

video_bp = Blueprint('video', __name__)

@video_bp.route("/video_feed")
def video_feed():
    def gen_frames():
        logger = LoggerService()
        logger.info("Starting video feed")
        try:
            with Camera() as cam:
                for frame in cam.frames():
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            logger.exception("Error in video feed")
            raise e
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@video_bp.route("/processed_feed")
def processed_feed():
    def gen_processed_frames():
        logger = LoggerService()
        logger.info("Starting processed video feed")
        try:
            with Camera() as cam:
                while True:
                    success, frame = cam.cap.read()
                    if not success:
                        break
                    height, width, _ = frame.shape
                    cv2.line(frame, (width // 2, 0), (width // 2, height), (0, 0, 255), 2)  # línea vertical roja
                    ret, buffer = cv2.imencode('.jpg', frame)
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        except Exception as e:
            logger.exception("Error in processed video feed")
            raise e
    return Response(gen_processed_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
