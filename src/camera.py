"""
Path: src/camera.py
"""

import cv2
from src.utils.logging.simple_logger import LoggerService

class Camera:
    "Clase para capturar video desde la cámara."
    def __init__(self, logger=None):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.logger = logger if logger else LoggerService()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cap.isOpened():
            self.cap.release()

    def frames(self):
        try:
            while True:
                success, frame = self.cap.read()
                if not success:
                    break
                ret, buffer = cv2.imencode('.jpg', frame)
                yield buffer.tobytes()
        except Exception as e:
            self.logger.exception("Error capturando frames")
            raise e
        finally:
            if self.cap.isOpened():
                self.cap.release()
