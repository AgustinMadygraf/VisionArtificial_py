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
from config import AppConfig

class AppFactory:
    def __init__(self, config: AppConfig):
        self.config = config

    def create_app(self):
        app = Flask(__name__, template_folder=self.config.TEMPLATE_FOLDER, static_folder=self.config.STATIC_FOLDER)
        app.register_blueprint(main_bp)
        app.register_blueprint(video_bp)
        return app
