"""
Path: src/services/frame_processor.py
"""

import cv2

class FrameProcessor:
    " "
    @staticmethod
    def process(frame):
        return process_frame(frame)


def process_frame(frame):
    "Procesa el marco de video para agregar líneas de referencia."
    height, width, _ = frame.shape
    # Dibujar línea vertical en el centro
    cv2.line(frame, (width // 2, 0), (width // 2, height), (0, 0, 255), 2)
    # Dibujar línea horizontal en el centro
    cv2.line(frame, (0, height // 2), (width, height // 2), (0, 0, 255), 2)
    return frame