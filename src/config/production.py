"""
Production configuration for the Flask application.
"""
from src.config.default import DefaultConfig
from src.config.video_config import VIDEO_CONFIG

class ProductionConfig(DefaultConfig):
    "Production configuration for the Flask application."
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'production-secret-key'
    VIDEO_CONFIG = VIDEO_CONFIG
