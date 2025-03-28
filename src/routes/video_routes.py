"""
Path: src/routes/video_routes.py
"""
import cv2
from flask import Blueprint, Response
from src.services.camera_service import CameraService
from src.services.frame_processor import FrameProcessor
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
            if process_function:
                # Flujo para video procesado utilizando cam.cap.read()
                while True:
                    success, frame = cam.cap.read()
                    if not success:
                        break
                    frame = process_function(frame)
                    _, buffer = cv2.imencode('.jpg', frame)
                    frame_bytes = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            else:
                # Flujo para video sin procesar utilizando el generador cam.frames()
                for frame in cam.frames():
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
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
