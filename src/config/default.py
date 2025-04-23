"""
Path: src/config/default.py
"""

class DefaultConfig:
    "Default configuration for the Flask application."
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'default-secret-key'
    # Configuración de parámetros para servicios
    SERVICES_CONFIG = {
        'video_capture_service': {
            'camera_index': 0,  # Ejemplo de parámetro para VideoCaptureService
        },
        'video_processing_service': {
            'processing_mode': 'fast',  # Ejemplo de parámetro para VideoProcessingService
        },
    }
