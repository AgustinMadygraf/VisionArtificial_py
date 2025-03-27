"""
Path: src/coordinator.py
"""

import threading
from src.factory import AppFactory
from config import AppConfig
from src.tkinter_view import TkinterViewer

class ApplicationCoordinator:
    def __init__(self):
        self.config = AppConfig()
        self.app_factory = AppFactory(self.config)
        self.flask_app = self.app_factory.create_app()
        self.tk_viewer = TkinterViewer()

    def run(self):
        flask_thread = threading.Thread(
            target=self.flask_app.run,
            kwargs={'debug': False, 'use_reloader': False}
        )
        flask_thread.start()
        self.tk_viewer.run()
