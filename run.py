"""
Path: run.py
Inicio de la aplicación.
Este módulo invoca main() de src/main.py, que orquesta la inicialización
y ejecución de los componentes.
"""

from src.coordinator import ApplicationCoordinator
from src.utils.logging.simple_logger import LoggerService

if __name__ == "__main__":
    try:
        logger = LoggerService()
        coordinator = ApplicationCoordinator(logger)
        coordinator.run()
    except KeyboardInterrupt:
        logger.info("Interrupción detectada (Ctrl+C). Cerrando aplicación...")
