"""
Path: src/services/frame_processor.py
"""
import cv2
from typing import Optional, Dict, Any
from src.config import DEFAULT_CONFIG
from src.services.configuration_service import ConfigurationService

class FrameProcessor:
    "Clase para procesar los marcos de video y agregar reglas de referencia."
    
    _config_service = None
    
    @classmethod
    def set_config_service(cls, config_service: ConfigurationService) -> None:
        """
        Establece el servicio de configuración para el procesador de frames.
        
        Args:
            config_service: Servicio de configuración a utilizar.
        """
        cls._config_service = config_service

    @staticmethod
    def process(frame, config_override=None):
        "Procesa el marco de video para agregar líneas de referencia y una regla horizontal."
        # Usar configuración proporcionada, o el servicio de configuración, o DEFAULT_CONFIG como fallback
        if config_override is not None:
            config = config_override
        elif FrameProcessor._config_service is not None:
            # Crear un objeto tipo AppConfig con los valores del servicio de configuración
            config = type('DynamicConfig', (), {})
            config.PIXELS_TO_UNITS = FrameProcessor._config_service.get(
                "PIXELS_TO_UNITS", DEFAULT_CONFIG.PIXELS_TO_UNITS
            )
        else:
            config = DEFAULT_CONFIG
            
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
            unit_value = x * config.PIXELS_TO_UNITS
            # Colocar el valor numérico de la posición con formato a un decimal
            cv2.putText(frame, f"{unit_value:.1f}", (x, height // 2 - tick_length),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1, cv2.LINE_AA)

        return frame
