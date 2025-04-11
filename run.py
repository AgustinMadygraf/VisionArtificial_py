"""
Path: run.py

"""

from src.main import create_app
from src.utils.logging.simple_logger import LoggerService

if __name__ == "__main__":
    try:
        logger = LoggerService()
        logger.debug("Starting the application using the App Factory.")
        app = create_app()
        logger.info("Aplicación iniciada.")
        app.run(debug=True)
    except KeyboardInterrupt:
        logger.info("Interrupción detectada (Ctrl+C). Cerrando aplicación...")
