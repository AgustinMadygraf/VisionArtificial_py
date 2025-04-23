"""
Path: src/config/default.py
"""

from src.config.video_config import VIDEO_CONFIG
from src.config.services_config import SERVICES_CONFIG

class DefaultConfig:
    "Default configuration for the Flask application."
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'default-secret-key'
    # Configuración de parámetros para servicios
    SERVICES_CONFIG = SERVICES_CONFIG
    VIDEO_CONFIG = VIDEO_CONFIG
