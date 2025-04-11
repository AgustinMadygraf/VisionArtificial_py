"""
VideoProcessingService: Implementación del servicio de procesamiento de video.
"""

import cv2
from typing import Any
from src.interfaces.IVideoProcessingService import IVideoProcessingService

class VideoProcessingService(IVideoProcessingService):
    """Implementación que maneja el procesamiento de frames de video."""
    
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
        if frame is None:
            raise ValueError("Frame cannot be None")
            
        try:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # pylint: disable=E1101
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)  # pylint: disable=E1101
            height, width, _ = frame.shape
            # Draw a red vertical line in the center
            cv2.line(frame, (width // 2, 0), (width // 2, height), (0, 0, 255), 2)  # pylint: disable=E1101
            # Draw a blue horizontal line in the center
            cv2.line(frame, (0, height // 2), (width, height // 2), (255, 0, 0), 2)  # pylint: disable=E1101
            return frame
        except Exception as e:
            raise ValueError(f"Error processing frame: {str(e)}") from e
