"""
Path: src/camera.py
Módulo que encapsula la lógica de captura de video. La clase Camera abre la cámara,
genera frames codificados y se asegura de liberar los recursos, facilitando pruebas
y mantenibilidad.
"""

import cv2
from src.utils.logging.simple_logger import LoggerService

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cap.isOpened():
            self.cap.release()

    def frames(self):
        logger = LoggerService()  # nuevo logger
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
