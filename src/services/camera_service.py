"""
Path: src/services/camera_service.py
"""

import threading
import time
from src.utils.logging.simple_logger import LoggerService
from src.services.http.video_formatter import VideoHTTPFormatter
from src.services.video.frame_buffer import FrameBuffer
from src.services.video.frame_producer import FrameProducer
from src.services.video.frame_consumer import FrameConsumer

logger = LoggerService()

def generate_frames(capture_service, processing_service, process=False):
    """
    Genera frames de video usando patrón productor-consumidor con buffer.
    Orquesta los componentes especializados para captura, procesamiento y formateo HTTP.
    """
    formatter = VideoHTTPFormatter()
    frame_buffer = FrameBuffer(maxsize=10)
    stop_event = threading.Event()
    producer = FrameProducer(capture_service, frame_buffer, stop_event)
    consumer = FrameConsumer(frame_buffer, processing_service, formatter, stop_event, process=process)

    # Iniciar hilos de productor y consumidor
    producer.start()
    consumer.start()
    try:
        while True:
            frame = consumer.get_formatted_frame()
            if frame:
                yield frame
            else:
                time.sleep(0.01)  # Espera breve para evitar busy-wait
    except RuntimeError as e:
        logger.error(f"RuntimeError during video capture: {e}")
    except Exception as specific_exception:
        logger.exception(f"Unexpected exception during video capture: {specific_exception}")
    finally:
        stop_event.set()
        producer.join()
        consumer.join()
        logger.info("Finalizando transmisión de video.")
