"""
Path: src/routes/video.py
"""

from flask import Blueprint, Response
from src.services.camera_service import generate_frames
from src.utils.logging.simple_logger import LoggerService

logger = LoggerService()

video_bp = Blueprint('video', __name__)

@video_bp.route('/video_original')
def video_original():
    "Ruta para el video original."
    return Response(
        generate_frames(process=False),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@video_bp.route('/video_process')
def video_process():
    "Ruta para el video procesado."
    return Response(
        generate_frames(process=True),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )
