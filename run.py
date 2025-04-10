"""
Path: run.py

"""

from src.main_flask import MainApp
from src.utils.logging.simple_logger import LoggerService

if __name__ == "__main__":
    try:
        logger = LoggerService()
        coordinator = MainApp(logger)
        coordinator.run()
    except KeyboardInterrupt:
        logger.info("Interrupción detectada (Ctrl+C). Cerrando aplicación...")
