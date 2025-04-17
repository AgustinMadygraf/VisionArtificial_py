"""
Path: run.py

"""

from src.main import MainApp
from src.utils.logging.simple_logger import LoggerService
from src.config.production import ProductionConfig  # Importa la configuración de producción si es necesario

if __name__ == "__main__":
    try:
        logger = LoggerService()
        # Cambia ProductionConfig por DefaultConfig según el entorno deseado
        main_app = MainApp(logger, config_object=ProductionConfig)
        main_app.run()
    except KeyboardInterrupt:
        logger.info("Interrupción detectada (Ctrl+C). Cerrando aplicación...")
