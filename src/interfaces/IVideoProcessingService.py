"""
Path: src/interfaces/IVideoProcessingService.py

Interfaz abstracta para servicios de procesamiento de video.
Define el contrato que deben cumplir todas las implementaciones
de servicios de procesamiento de video en el sistema.
"""

import abc
from typing import Any

class IVideoProcessingService(abc.ABC):
    """
    Interfaz para un servicio de procesamiento de video.
    Define el contrato que deben cumplir las implementaciones,
    facilitando la inyección de dependencias y la sustitución
    de implementaciones para diferentes algoritmos de procesamiento.
    """
    
    @abc.abstractmethod
    def process_frame(self, frame: Any) -> Any:
        """
        Procesa un frame de video aplicando transformaciones.
        
        Args:
            frame: El frame a procesar.
            
        Returns:
            Any: El frame procesado.
            
        Raises:
            ValueError: Si el frame no tiene un formato válido o es None.
        """
        pass