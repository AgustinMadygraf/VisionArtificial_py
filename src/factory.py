"""
Path: src/factory.py

La fábrica de la aplicación se encarga de:
 - Inicializar el objeto Flask.
 - Registrar blueprints que encapsulan rutas y lógicas de cada módulo.
   * main_routes: Maneja las rutas principales.
   * video_routes: Gestiona rutas relacionadas con funcionalidades de video.
 
Esta organización permite una separación clara entre la lógica de negocio y la presentación.
"""

from flask import Flask
from src.routes.main_routes import main_bp
from src.routes.video_routes import video_bp
from src.config import AppConfig
from src.utils.logging.simple_logger import LoggerService

class AppFactory:
    " Clase responsable de crear la aplicación Flask."
    def __init__(self, config: AppConfig , logger:LoggerService ):
        self.config = config
        self.logger = logger

    def create_app(self):
        app = Flask(__name__, template_folder=self.config.TEMPLATE_FOLDER, static_folder=self.config.STATIC_FOLDER)
        app.register_blueprint(main_bp)
        self.logger.info("Blueprint 'main_routes' registrado correctamente.")
        app.register_blueprint(video_bp)
        self.logger.info("Blueprint 'video_routes' registrado correctamente.")
        return app
