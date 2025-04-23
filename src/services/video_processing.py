"""
VideoProcessingService: Implementación del servicio de procesamiento de video.
"""

from typing import Any
import cv2
from src.interfaces.i_video_processing_service import IVideoProcessingService
from src.services.processors.grayscale_processor import GrayscaleProcessor
from src.services.processors.registry import processor_registry

class VideoProcessingService(IVideoProcessingService):
    """Implementación que maneja el procesamiento de frames de video."""

    def __init__(self, processing_mode=None, use_gpu=False, processor_name='grayscale', **kwargs):
        """
        Inicializa el servicio de procesamiento de video.
        Args:
            processing_mode (str, opcional): Modo de procesamiento ('fast', 'accurate', etc).
            use_gpu (bool, opcional): Si se debe usar GPU (no implementado, 
            solo para compatibilidad).
            processor_name (str, opcional): Nombre del procesador a usar.
            **kwargs: Otros parámetros de configuración ignorados por compatibilidad.
        """
        self.processing_mode = processing_mode
        self.use_gpu = use_gpu
        # Selección dinámica de procesador
        try:
            processor_cls = processor_registry.get(processor_name)
        except Exception:
            processor_cls = processor_registry.get('grayscale')
        self.processor = processor_cls()

    def process_frame(self, frame: Any) -> Any:
        """
        Procesa un frame de video usando la estrategia configurada.
        
        Args:
            frame: El frame a procesar.
            
        Returns:
            Any: El frame procesado.
            
        Raises:
            ValueError: Si el frame no tiene un formato válido o es None.
        """
        return self.processor.process_frame(frame)
