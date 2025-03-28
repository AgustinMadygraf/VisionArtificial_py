"""
Path: src/services/camera_service.py
"""

from src.camera import Camera

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
