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
        self.logger = logger if logger else LoggerService()
        self.cap = None
        self._initialize_camera()

    def _initialize_camera(self):
        """Try initializing the camera with different backends, and fallback to default."""
        backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_VFW]
        for backend in backends:
            self.cap = cv2.VideoCapture(0, backend)
            if self.cap.isOpened():
                self.logger.info(f"Camera initialized successfully with backend: {backend}")
                return
            else:
                self.logger.warning(f"Failed to initialize camera with backend: {backend}")

        # Fallback to default initialization without specifying a backend
        self.cap = cv2.VideoCapture(0)
        if self.cap.isOpened():
            self.logger.info("Camera initialized successfully with default backend.")
        else:
            self.logger.error("Unable to initialize camera with any backend, including default.")
            raise RuntimeError("Unable to initialize camera with any backend, including default.")

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
