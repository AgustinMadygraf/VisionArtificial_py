"""
VideoCaptureService: Implementación del servicio de captura de video.
"""

from typing import Any
import cv2
from src.interfaces.IVideoCaptureService import IVideoCaptureService

class VideoCaptureService(IVideoCaptureService):
    """Implementación que maneja la captura de video desde una cámara."""

    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.camera = None

    def open_camera(self) -> None:
        """
        Abre la cámara para la captura de video.
        
        Raises:
            RuntimeError: Si no se puede abrir la cámara.
        """
        self.camera = cv2.VideoCapture(self.camera_index, cv2.CAP_ANY)  # pylint: disable=E1101
        if not self.camera.isOpened():
            raise RuntimeError(f"Cannot open camera with index {self.camera_index}")

    def read_frame(self) -> Any:
        """
        Lee un frame de la cámara.
        
        Returns:
            Any: El frame capturado.
            
        Raises:
            RuntimeError: Si la cámara no está abierta o si falla la lectura del frame.
        """
        if not self.camera:
            raise RuntimeError("Camera is not opened")
        success, frame = self.camera.read()
        if not success:
            raise RuntimeError("Failed to read frame from camera")
        return frame

    def release_camera(self) -> None:
        """
        Libera los recursos de la cámara.
        """
        if self.camera:
            self.camera.release()
            self.camera = None
