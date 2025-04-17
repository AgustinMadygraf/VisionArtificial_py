"""
Path: src/services/camera_service.py
"""

import cv2
from src.utils.logging.simple_logger import LoggerService

logger = LoggerService()

def generate_frames(capture_service, processing_service, process=False):
    """
    Genera frames de video, usando el gestor de contexto del servicio de captura
    para garantizar la liberación automática de la cámara.
    El acceso a la cámara está protegido contra concurrencia.
    Args:
        capture_service: Servicio de captura de video (debe implementar 
        context manager y protección concurrente).
        processing_service: Servicio de procesamiento de frames.
        process (bool): Si es True, procesa cada frame antes de enviarlo.
    Yields:
        bytes: Frame codificado en JPEG listo para transmisión HTTP.
    """
    try:
        with capture_service:
            while True:
                frame = capture_service.read_frame()

                if process:
                    frame = processing_service.process_frame(frame)

                _, buffer = cv2.imencode('.jpg', frame)  # pylint: disable=E1101
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    except RuntimeError as e:
        logger.error(f"RuntimeError during video capture: {e}")
    except (cv2.error, ValueError) as specific_exception:
        logger.exception(f"Unexpected exception during video capture: {specific_exception}")
    finally:
        logger.info("Finalizando transmisión de video.")
