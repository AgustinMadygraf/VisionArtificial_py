"""
Módulo de Factoría de Servicios

Este módulo centraliza la creación de instancias de servicios,
facilitando la inyección de dependencias y mejorando la modularidad.
"""

from src.services.video_capture_service import VideoCaptureService
from src.services.video_processing import VideoProcessingService

def get_video_capture_service():
    """
    Devuelve una instancia de VideoCaptureService.

    Returns:
        VideoCaptureService: Instancia del servicio de captura de video.
    """
    return VideoCaptureService()

def get_video_processing_service():
    """
    Devuelve una instancia de VideoProcessingService.

    Returns:
        VideoProcessingService: Instancia del servicio de procesamiento de video.
    """
    return VideoProcessingService()