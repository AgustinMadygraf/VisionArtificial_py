"""
Path: src/main.py
"""

from flask import Flask
from flask_cors import CORS
from src.config.default import DefaultConfig
from src.routes.home import home_bp
from src.routes.video import video_bp
# Importa aquí futuros Blueprints...

class MainApp:
    "Clase principal de la aplicación Flask."
    def __init__(self, logger, config_object=None):
        self.logger = logger
        self.app = self.create_app(config_object)

    def run(self):
        "Inicia la aplicación Flask."
        self.logger.info("Aplicación iniciada.")
        self.app.run(debug=True)

    def create_app(self, config_object=None):
        """Factory function to create and configure the Flask application."""
        if config_object is None:
            config_object = DefaultConfig
        app = Flask(__name__, template_folder="../templates", static_folder="../static")
        CORS(app)  # Habilita CORS para todas las rutas
        app.config.from_object(config_object)

        # Registro de Blueprints principales
        app.register_blueprint(home_bp)
        app.register_blueprint(video_bp)
        # Registra aquí futuros Blueprints, por ejemplo:
        # app.register_blueprint(admin_bp)

        return app
