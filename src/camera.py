"""
Path: src/camera.py
"""

import cv2
from src.utils.logging.simple_logger import LoggerService

_logger_service_instance = LoggerService()

def get_logger_instance():
    return _logger_service_instance


class Camera:
    "Clase para capturar video desde la cámara."
    def __init__(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cap.isOpened():
            self.cap.release()

    def frames(self):
        logger = get_logger_instance()
        try:
            while True:
                success, frame = self.cap.read()
                if not success:
                    break
                ret, buffer = cv2.imencode('.jpg', frame)
                yield buffer.tobytes()
        except Exception as e:
            logger.exception("Error capturing frame")
            raise e
