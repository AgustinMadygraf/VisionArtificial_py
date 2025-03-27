"""
Path: src/coordinator.py
"""

import threading
from src.factory import AppFactory
from src.config import AppConfig
from src.tkinter_view import TkinterViewer
from src.utils.logging.simple_logger import get_logger_instance

logger = get_logger_instance()

class ApplicationCoordinator:
    "Clase coordinadora que orquesta la inicialización y ejecución de la aplicación."
    def __init__(self):
        self.config = AppConfig()
        logger.debug("Configuración de la aplicación: %s", self.config.__dict__)
        self.app_factory = AppFactory(self.config)
        self.flask_app = self.app_factory.create_app()
        self.tk_viewer = TkinterViewer()

    def run(self):
        logger.info("Iniciando servidor Flask...")
        flask_thread = threading.Thread(
            target=self.flask_app.run,
            kwargs={'debug': False, 'use_reloader': False}
        )
        flask_thread.start()
        logger.info("Servidor Flask iniciado.")
        logger.info("Iniciando interfaz Tkinter...")
        self.tk_viewer.run()
        logger.info("Interfaz Tkinter cerrada.")
