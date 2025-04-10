"""
Path: run.py

"""

from src.main import MainApp
from src.utils.logging.simple_logger import LoggerService

if __name__ == "__main__":
    try:
        logger = LoggerService()
        main_app = MainApp(logger)
        main_app.run()
    except KeyboardInterrupt:
        logger.info("Interrupción detectada (Ctrl+C). Cerrando aplicación...")
