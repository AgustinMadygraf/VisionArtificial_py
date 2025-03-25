"""
Path: src/routes/video_routes.py
"""

from flask import Blueprint, Response
from src.camera import Camera
from src.utils.logging.simple_logger import LoggerService

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
