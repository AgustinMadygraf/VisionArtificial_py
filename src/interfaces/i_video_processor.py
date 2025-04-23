"""
Interfaz para algoritmos de procesamiento de video.
Todas las implementaciones deben cumplir este contrato.
"""
from typing import Any
from abc import ABC, abstractmethod

class IVideoProcessor(ABC):
    @abstractmethod
    def process_frame(self, frame: Any) -> Any:
        """
        Procesa un frame de video y devuelve el resultado.
        Args:
            frame: El frame a procesar.
        Returns:
            Any: El frame procesado.
        """
        pass
