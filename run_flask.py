"""
Path: run.py

"""

from src.main import MainApp
from src.utils.logging.simple_logger import LoggerService
from src.config.production import ProductionConfig
from src.core.service_factory import configure_service_params

if __name__ == "__main__":
    try:
        logger = LoggerService()
        # Configurar parámetros de servicios desde la configuración activa
        configure_service_params(ProductionConfig.SERVICES_CONFIG)
        main_app = MainApp(logger, config_object=ProductionConfig)
        main_app.run()
    except KeyboardInterrupt:
        logger.info("Interrupción detectada (Ctrl+C). Cerrando aplicación...")
