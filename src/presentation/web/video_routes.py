"""
Path: src/routes/video_routes.py
"""
# Suppress type-checking errors for cv2 members
import cv2  # type: ignore
from flask import Blueprint, Response, jsonify
from src.core.shared_service import SharedService
from src.utils.logging.simple_logger import LoggerService

video_bp = Blueprint('video', __name__)

def get_logger():
    "Función para obtener el logger."
    return getattr(video_bp, 'logger', None) or LoggerService()

shared_service = SharedService(get_logger())  # SharedService is already instantiated aquí

def generate_frames(process_function=None):
    "Genera frames, aplicando la función de procesamiento si se proporciona."
    logger = get_logger()
    logger.info("Iniciando el flujo de video")
    try:
        shared_service.initialize()  # Inicializar servicios compartidos
        camera = shared_service.get_camera_service()  # Obtener servicio de cámara
        while True:
            success, frame = camera.cap.read()
            if not success:
                break
            if process_function:
                frame = process_function(frame)  # Usar función de procesamiento
            _, buffer = cv2.imencode('.jpg', frame)  # type: ignore
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    except Exception as e:
        logger.exception("Error en el flujo de video")
        raise e
    finally:
        shared_service.shutdown()  # Finalizar servicios compartidos

@video_bp.route("/video_feed")
def video_feed():
    "Ruta para el flujo de video sin procesar."
    try:
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        logger = get_logger()
        logger.exception("Error en el endpoint /video_feed")
        return jsonify({"error": "Error al generar el flujo de video"}), 500

@video_bp.route("/processed_feed")
def processed_feed():
    "Ruta para el flujo de video procesado."
    return Response(generate_frames(shared_service.get_frame_processor().process), mimetype='multipart/x-mixed-replace; boundary=frame')

@video_bp.errorhandler(Exception)
def handle_exception(e):
    "Manejo centralizado de excepciones en los endpoints de video."
    logger = get_logger()
    logger.exception("Error no controlado en un endpoint de video")
    return jsonify({"error": "Ocurrió un error interno en el servidor"}), 500
