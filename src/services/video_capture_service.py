"""
VideoCaptureService: Implementación del servicio de captura de video.
"""

from typing import Any
import threading
import cv2
from src.interfaces.i_video_capture_service import IVideoCaptureService

class VideoCaptureService(IVideoCaptureService):
    """
    Implementación que maneja la captura de video desde una cámara.
    
    Ahora implementa un gestor de contexto (with) y protección 
    contra acceso concurrente usando threading.Lock.
    Esto garantiza la liberación automática de la cámara y 
    evita conflictos en escenarios multiusuario.
    """

    def __init__(self, camera_index=0):
        # Lock para acceso concurrente seguro a la cámara
        self._lock = threading.Lock()
        self.camera_index = camera_index
        self.camera = None

    def open_camera(self) -> None:
        """
        Abre la cámara para la captura de video. Protegido por 
        lock para evitar conflictos concurrentes.
        
        Raises:
            RuntimeError: Si no se puede abrir la cámara.
        """
        with self._lock:
            self.camera = cv2.VideoCapture(self.camera_index, cv2.CAP_ANY)  # pylint: disable=E1101
            if not self.camera.isOpened():
                raise RuntimeError(f"Cannot open camera with index {self.camera_index}")

    def read_frame(self) -> Any:
        """
        Lee un frame de la cámara. Protegido por lock para evitar condiciones de carrera.
        
        Returns:
            Any: El frame capturado.
            
        Raises:
            RuntimeError: Si la cámara no está abierta o si falla la lectura del frame.
        """
        with self._lock:
            if not self.camera:
                raise RuntimeError("Camera is not opened")
            success, frame = self.camera.read()
            if not success:
                raise RuntimeError("Failed to read frame from camera")
            return frame

    def release_camera(self) -> None:
        """
        Libera los recursos de la cámara. Protegido por lock.
        """
        with self._lock:
            if self.camera:
                self.camera.release()
                self.camera = None

    def __enter__(self):
        """
        Permite el uso de VideoCaptureService como gestor de contexto (with statement).
        Abre la cámara automáticamente al entrar en el contexto.
        """
        self.open_camera()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Libera la cámara automáticamente al salir del contexto, incluso si ocurre una excepción.
        """
        self.release_camera()
