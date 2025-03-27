"""
Path: src/coordinator.py
"""

import threading
import sys
from src.factory import AppFactory
from src.config import AppConfig
from src.tkinter_view import TkinterViewer

class ApplicationCoordinator:
    "Clase coordinadora que orquesta la inicialización y ejecución de la aplicación."
    def __init__(self, logger):
        self.logger = logger
        self.config = AppConfig()
        self.logger.debug("Configuración de la aplicación: %s", self.config.__dict__)
        self.app_factory = AppFactory(self.config, self.logger)
        self.flask_app = self.app_factory.create_app()
        self.tk_viewer = TkinterViewer(self.logger)

    def run_flask(self):
        self.logger.info("Iniciando servidor Flask...")
        flask_thread = threading.Thread(
            target=self.flask_app.run,
            kwargs={'debug': False, 'use_reloader': False}
        )
        flask_thread.start()
        self.logger.info("Servidor Flask iniciado.")
        return flask_thread

    def run_tkinter(self):
        self.logger.info("Iniciando interfaz Tkinter...")
        self.tk_viewer.run()
        self.logger.info("Interfaz Tkinter cerrada.")

    def run(self):
        flask_thread = self.run_flask()
        self.run_tkinter()
        self.logger.info("Cerrando servidor Flask...")
        import requests
        try:
            requests.get("http://127.0.0.1:5000/shutdown")
        except Exception as e:
            self.logger.exception("Error al enviar solicitud de shutdown a Flask")
        self.logger.info("Esperando a que el hilo del servidor Flask finalice...")
        flask_thread.join()
        self.logger.info("Servidor Flask cerrado.")
        self.logger.info("Aplicación cerrada.")
        sys.exit(0)

