"""
Path: src/routes/video_routes.py
"""
# Suppress type-checking errors for cv2 members
import cv2  # type: ignore
from flask import Blueprint, Response
from src.core.camera_service import CameraService
from src.core.frame_processor import FrameProcessor
from src.utils.logging.simple_logger import LoggerService

video_bp = Blueprint('video', __name__)

def get_logger():
    "Función para obtener el logger."
    return getattr(video_bp, 'logger', None) or LoggerService()

def generate_frames(process_function=None):
    "Genera frames, aplicando la función de procesamiento si se proporciona."
    logger = get_logger()
    logger.info("Iniciando el flujo de video")
    try:
        with CameraService(logger) as cam:
            while True:
                success, frame = cam.cap.read()
                if not success:
                    break
                if process_function:
                    frame = FrameProcessor.process(frame)  # Centraliza el procesamiento en FrameProcessor
                _, buffer = cv2.imencode('.jpg', frame)  # type: ignore
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    except Exception as e:
        logger.exception("Error en el flujo de video")
        raise e

@video_bp.route("/video_feed")
def video_feed():
    "Ruta para el flujo de video sin procesar."
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@video_bp.route("/processed_feed")
def processed_feed():
    "Ruta para el flujo de video procesado."
    return Response(generate_frames(FrameProcessor.process), mimetype='multipart/x-mixed-replace; boundary=frame')
