"""
Path: src/services/camera_service.py
"""

import cv2
from src.services.video_capture_service import VideoCaptureService
from src.services.video_processing import VideoProcessingService
from src.utils.logging.simple_logger import LoggerService

logger = LoggerService()

def generate_frames(process=False):
    """Generates video frames, optionally processing them."""
    capture_service = VideoCaptureService()
    processing_service = VideoProcessingService()

    try:
        capture_service.open_camera()
        while True:
            frame = capture_service.read_frame()

            if process:
                frame = processing_service.process_frame(frame)

            _, buffer = cv2.imencode('.jpg', frame)  # pylint: disable=E1101
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    except RuntimeError as e:
        logger.error(f"RuntimeError during video capture: {e}")
    except (cv2.error, ValueError) as specific_exception: # pylint: disable=E1101
        logger.exception(f"Unexpected exception during video capture: {specific_exception}")
    finally:
        logger.info("Releasing the camera.")
        capture_service.release_camera()
