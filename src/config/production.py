"""
Production configuration for the Flask application.
"""
from src.config.default import DefaultConfig

class ProductionConfig(DefaultConfig):
    "Production configuration for the Flask application."
    DEBUG = False
    SECRET_KEY = 'production-secret-key'
