"""
Path: src/routes/video.py
"""

from flask import Blueprint, Response
from src.services.camera_service import generate_frames
from src.utils.logging.simple_logger import LoggerService
from src.services.video_capture_service import VideoCaptureService
from src.services.video_processing import VideoProcessingService

logger = LoggerService()

video_bp = Blueprint('video', __name__)

@video_bp.route('/video_original')
def video_original():
    """Route for the original video feed."""
    try:
        capture_service = VideoCaptureService()
        processing_service = VideoProcessingService()
        return Response(
            generate_frames(capture_service, processing_service, process=False),
            mimetype='multipart/x-mixed-replace; boundary=frame'
        )
    except RuntimeError as e:
        logger.error(f"Error in /video_original route: {e}")
        return Response("Error accessing the video stream.", status=500)

@video_bp.route('/video_process')
def video_process():
    """Route for the processed video feed."""
    try:
        capture_service = VideoCaptureService()
        processing_service = VideoProcessingService()
        return Response(
            generate_frames(capture_service, processing_service, process=True),
            mimetype='multipart/x-mixed-replace; boundary=frame'
        )
    except RuntimeError as e:
        logger.error(f"Error in /video_process route: {e}")
        return Response("Error accessing the processed video stream.", status=500)
