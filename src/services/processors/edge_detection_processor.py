"""
Procesador de video que detecta bordes usando Canny.
"""
import cv2
from src.services.processors.base_processor import BaseVideoProcessor

class EdgeDetectionProcessor(BaseVideoProcessor):
    def process_frame(self, frame):
        if frame is None:
            raise ValueError("Frame cannot be None")
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            # Convertir a BGR para mantener el formato
            edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            return edges_bgr
        except Exception as e:
            raise ValueError(f"Error processing frame (edge detection): {str(e)}") from e
