"""
Path: src/services/frame_processor.py
"""
import cv2
from typing import Optional, Dict, Any

class FrameProcessor:
    "Clase para procesar los marcos de video y agregar reglas de referencia."
    
    _config_service: Optional[object] = None  # Cambiar el tipo a un objeto genérico
    
    @classmethod
    def set_config_service(cls, config_service) -> None:
        """
        Establece el servicio de configuración para el procesador de frames.
        
        Args:
            config_service: Servicio de configuración a utilizar.
        """
        cls._config_service = config_service

    @staticmethod
    def process(frame):
        """Procesa el marco de video para agregar líneas de referencia y una regla horizontal."""
        if FrameProcessor._config_service is None:
            raise ValueError("ConfigurationService must be set before processing frames.")

        # Obtener configuración dinámica del servicio
        pixels_to_units = FrameProcessor._config_service.get("PIXELS_TO_UNITS")

        height, width, _ = frame.shape

        # Dibujar línea vertical en el centro
        cv2.line(frame, (width // 2, 0), (width // 2, height), (0, 0, 255), 1)

        # Dibujar línea horizontal en el centro
        cv2.line(frame, (0, height // 2), (width, height // 2), (0, 255, 0), 2)

        # Construir la regla horizontal: agregar marcas cada 50 píxeles
        tick_interval = 50
        tick_length = 10
        for x in range(0, width, tick_interval):
            # Dibujar una pequeña marca vertical en la línea horizontal
            cv2.line(frame, (x, height // 2 - tick_length // 2),
                           (x, height // 2 + tick_length // 2), (255, 0, 0), 1)
            # Convertir la posición en píxeles a la unidad deseada
            unit_value = x * pixels_to_units
            # Colocar el valor numérico de la posición con formato a un decimal
            cv2.putText(frame, f"{unit_value:.1f}", (x, height // 2 - tick_length),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1, cv2.LINE_AA)

        return frame
