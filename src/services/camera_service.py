"""
Path: src/services/camera_service.py
"""

import cv2
from src.utils.logging.simple_logger import LoggerService

class CameraService:
    "Clase de servicio para manejar la cámara."
    def __init__(self, logger):
        self.logger = logger
        self.camera = None

    def __enter__(self):
        self.logger.debug("Inicializando cámara con CameraService")
        self.camera = Camera(self.logger)
        return self.camera

    def __exit__(self, exc_type, exc_value, traceback):
        if self.camera is not None:
            try:
                self.camera.cap.release()
                self.logger.info("Cámara liberada por CameraService")
            except RuntimeError:
                self.logger.exception("Error al liberar la cámara en CameraService")
        return False

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
        "Generador de frames de video."
        try:
            while True:
                success, frame = self.cap.read()
                if not success:
                    break
                _, buffer = cv2.imencode('.jpg', frame)
                yield buffer.tobytes()
        except Exception as e:
            self.logger.exception("Error capturando frames")
            raise e
        finally:
            if self.cap.isOpened():
                self.cap.release()
