"""
Path: src/routes/video_routes.py
"""

import cv2
from flask import Blueprint, Response
from src.services.camera_service import CameraService
from src.services.frame_processor import FrameProcessor
from src.utils.logging.simple_logger import LoggerService

video_bp = Blueprint('video', __name__)

def get_logger():
    return getattr(video_bp, 'logger', None) or LoggerService()

@video_bp.route("/video_feed")
def video_feed():
    def gen_frames():
        logger = get_logger()
        logger.info("Starting video feed")
        try:
            with CameraService(logger) as cam:
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
        logger = get_logger()
        logger.info("Starting processed video feed")
        try:
            with CameraService(logger) as cam:
                while True:
                    success, frame = cam.cap.read()
                    if not success:
                        break
                    frame = FrameProcessor.process(frame)
                    ret, buffer = cv2.imencode('.jpg', frame)
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        except Exception as e:
            logger.exception("Error in processed video feed")
            raise e
    return Response(gen_processed_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
