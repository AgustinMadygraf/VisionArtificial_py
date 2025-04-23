"""
Procesador de video que convierte los frames a escala de grises y dibuja líneas.
"""
import cv2
from src.services.processors.base_processor import BaseVideoProcessor

class GrayscaleProcessor(BaseVideoProcessor):
    "Esta clase procesa frames de video convirtiéndolos a escala de grises y dibujando líneas."
    def process_frame(self, frame):
        if frame is None:
            raise ValueError("Frame cannot be None")
        try:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # pylint: disable=E1101
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR) # pylint: disable=E1101
            height, width, _ = frame.shape
            # Draw a red vertical line in the center
            cv2.line(frame, (width // 2, 0), (width // 2, height), (0, 0, 255), 2) # pylint: disable=E1101
            # Draw a blue horizontal line in the center
            cv2.line(frame, (0, height // 2), (width, height // 2), (255, 0, 0), 2) # pylint: disable=E1101
            return frame
        except Exception as e:
            raise ValueError(f"Error processing frame: {str(e)}") from e
