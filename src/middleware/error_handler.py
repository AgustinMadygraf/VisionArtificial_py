from flask import jsonify
from werkzeug.exceptions import HTTPException
import traceback
from src.exceptions.base import VisionArtificialError
from src.exceptions.service import ServiceError
from src.exceptions.config import ConfigError


def register_error_handlers(app, logger=None):
    """
    Registra manejadores globales de errores en la app Flask.
    """
    @app.errorhandler(VisionArtificialError)
    def handle_vision_error(error):
        response = {
            "error": str(error),
            "type": error.__class__.__name__
        }
        if logger:
            logger.error(f"VisionArtificialError: {error}")
        return jsonify(response), 400

    @app.errorhandler(ServiceError)
    def handle_service_error(error):
        response = {
            "error": str(error),
            "type": error.__class__.__name__
        }
        if logger:
            logger.error(f"ServiceError: {error}")
        return jsonify(response), 503

    @app.errorhandler(ConfigError)
    def handle_config_error(error):
        response = {
            "error": str(error),
            "type": error.__class__.__name__
        }
        if logger:
            logger.error(f"ConfigError: {error}")
        return jsonify(response), 500

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        response = {
            "error": error.description,
            "type": error.__class__.__name__
        }
        if logger:
            logger.error(f"HTTPException: {error}")
        return jsonify(response), error.code

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        response = {
            "error": "Ocurrió un error interno inesperado.",
            "type": error.__class__.__name__,
            "details": str(error)
        }
        if logger:
            logger.error(f"Unhandled Exception: {error}\n{traceback.format_exc()}")
        return jsonify(response), 500
