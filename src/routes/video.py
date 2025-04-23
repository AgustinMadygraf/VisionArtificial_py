"""
Path: src/routes/video.py
"""

from flask import Blueprint, Response, current_app
from src.services.camera_service import generate_frames
from src.utils.logging.simple_logger import LoggerService

logger = LoggerService()

# Asignar prefijo de URL para el dominio de video
video_bp = Blueprint('video', __name__, url_prefix='/video')

@video_bp.route('/original')
def video_original():
    """Route for the original video feed."""
    container = current_app.container
    capture_service = container.video_capture_service()
    processing_service = container.video_processing_service()
    return Response(
        generate_frames(capture_service, processing_service, process=False),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@video_bp.route('/process')
def video_process():
    """Route for the processed video feed."""
    container = current_app.container
    capture_service = container.video_capture_service()
    processing_service = container.video_processing_service()
    return Response(
        generate_frames(capture_service, processing_service, process=True),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )
