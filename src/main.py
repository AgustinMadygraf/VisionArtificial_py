"""
Path: src/main.py
"""

from flask import Flask
from src.config.default import DefaultConfig
from src.routes.home import home_bp
from src.routes.video import video_bp



class MainApp:
    "Clase principal de la aplicación Flask."
    def __init__(self, logger):
        self.logger = logger
        self.app = self.create_app()

    def run(self):
        "Inicia la aplicación Flask."
        self.logger.info("Aplicación iniciada.")
        self.app.run(debug=True)

    def create_app(self):
        """Factory function to create and configure the Flask application."""
        config_class = DefaultConfig()
        app = Flask(__name__, template_folder="../templates", static_folder="../static")
        app.config.from_object(config_class)

        app.register_blueprint(home_bp)
        app.register_blueprint(video_bp)

        return app
