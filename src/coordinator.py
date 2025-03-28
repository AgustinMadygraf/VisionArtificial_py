"""
Path: src/coordinator.py
"""

import threading
import requests
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
        self.shutdown_event = threading.Event()

    def run_flask(self):
        "Inicia el servidor Flask en un hilo separado."
        self.logger.info("Iniciando servidor Flask...")
        flask_thread = threading.Thread(
            target=self.flask_app.run,
            kwargs={'debug': False, 'use_reloader': False},
            daemon=True
        )
        flask_thread.start()
        self.logger.info("Servidor Flask iniciado.")
        return flask_thread

    def run_tkinter(self):
        "Inicia la interfaz gráfica de Tkinter."
        self.logger.info("Iniciando interfaz Tkinter...")
        self.tk_viewer.run()
        self.logger.info("Interfaz Tkinter cerrada.")

    def run(self):
        "Inicia la aplicación coordinando el servidor Flask y la interfaz Tkinter."
        flask_thread = self.run_flask()
        self.run_tkinter()
        self.logger.info("Señalizando cierre de la aplicación...")
        self.shutdown_event.set()
        self.logger.info("Cerrando servidor Flask...")
        try:
            requests.get("http://127.0.0.1:5000/shutdown", timeout=1)
        except requests.exceptions.ConnectionError:
            self.logger.info("Shutdown request sent; connection closed as expected.")
        except requests.exceptions.RequestException:
            self.logger.exception("Error al enviar solicitud de shutdown a Flask")
        self.logger.info("Esperando a que el hilo del servidor Flask finalice...")
        flask_thread.join()
        self.logger.info("Servidor Flask cerrado.")
        self.logger.info("Aplicación cerrada.")
        # Removed sys.exit(0) to allow controlled shutdown
