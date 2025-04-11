"""
Path: src/services/video_processing.py 
"""

from typing import Any
import cv2
from src.interfaces.i_video_processing_service import IVideoProcessingService
from src.utils.logging.simple_logger import LoggerService

logger = LoggerService()

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
            logger.debug("Received a None frame for processing.")
            raise ValueError("Frame cannot be None")

        try:
  #          logger.debug("Converting frame to grayscale.")
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # pylint: disable=E1101
  #          logger.debug("Converting frame back to BGR format.")
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)  # pylint: disable=E1101
            height, width, _ = frame.shape
 #           logger.debug("Frame dimensions: %dx%d", width, height)
 #           logger.debug("Drawing red vertical line in the center.")
            cv2.line(frame, (width // 2, 0), (width // 2, height), (0, 0, 255), 2)  # pylint: disable=E1101
#            logger.debug("Drawing blue horizontal line in the center.")
            cv2.line(frame, (0, height // 2), (width, height // 2), (255, 0, 0), 2)  # pylint: disable=E1101
            return frame
        except Exception as e:
            raise ValueError(f"Error processing frame: {str(e)}") from e
