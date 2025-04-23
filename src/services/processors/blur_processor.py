"""
Procesador de video que aplica desenfoque gaussiano.
"""
import cv2
from src.services.processors.base_processor import BaseVideoProcessor

class BlurProcessor(BaseVideoProcessor):
    def process_frame(self, frame):
        if frame is None:
            raise ValueError("Frame cannot be None")
        try:
            blurred = cv2.GaussianBlur(frame, (15, 15), 0)
            return blurred
        except Exception as e:
            raise ValueError(f"Error processing frame (blur): {str(e)}") from e
