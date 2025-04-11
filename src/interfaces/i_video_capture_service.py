"""
Path: src/interfaces/IVideoCaptureService.py
"""

import abc
from typing import Any

class IVideoCaptureService(abc.ABC):
    """
    Interfaz para un servicio de captura de video.
    Define el contrato que deben cumplir las implementaciones,
    facilitando la inyección de dependencias y la futura extensión.
    """

    @abc.abstractmethod
    def open_camera(self) -> None:
        """
        Abre la cámara para la captura de video.
        
        Raises:
            RuntimeError: Si no se puede abrir la cámara.
        """
        pass

    @abc.abstractmethod
    def read_frame(self) -> Any:
        """
        Lee un frame de la cámara.
        
        Returns:
            Any: El frame capturado.
            
        Raises:
            RuntimeError: Si la cámara no está abierta o si falla la lectura del frame.
        """
        pass

    @abc.abstractmethod
    def release_camera(self) -> None:
        """
        Libera los recursos de la cámara.
        """
        pass
