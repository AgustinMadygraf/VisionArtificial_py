"""
Path: run.py

"""

from src.main import MainApp
from src.utils.logging.simple_logger import LoggerService
from src.config.config_loader import load_config
from src.core.service_factory import configure_service_params

if __name__ == "__main__":
    try:
        logger = LoggerService()
        ConfigClass = load_config()
        configure_service_params(ConfigClass.SERVICES_CONFIG)
        main_app = MainApp(logger, config_object=ConfigClass)
        main_app.run()
    except KeyboardInterrupt:
        logger.info("Interrupción detectada (Ctrl+C). Cerrando aplicación...")
