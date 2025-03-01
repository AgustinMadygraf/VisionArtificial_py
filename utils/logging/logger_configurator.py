"""
Configurador de logging para la aplicación.
Proporciona una API unificada para configurar el logging.
"""

import logging
import logging.handlers
import os
from typing import Optional, List, Any

# Singleton para acceso global al logger
_APP_LOGGER: Optional[logging.Logger] = None


class LoggerConfigurator:
    """Configurador de logging para la aplicación."""

    def __init__(self, log_path: str = "logs", log_level: int = logging.INFO):
        """
        Inicializa el configurador de logging.
        
        Args:
            log_path: Ruta donde se almacenarán los logs
            log_level: Nivel de logging predeterminado
        """
        self.log_path = log_path
        self.log_level = log_level
        self.filters = []

        # Crear el directorio de logs si no existe
        os.makedirs(log_path, exist_ok=True)

    def register_filter(self, filter_class: Any) -> None:
        """
        Registra un filtro para usarlo en la configuración.
        
        Args:
            filter_class: Clase del filtro a instanciar
        """
        self.filters.append(filter_class())

    def configure(self, filters: Optional[List[Any]] = None) -> logging.Logger:
        """
        Configura y devuelve un logger con los filtros proporcionados.
        
        Args:
            filters: Lista opcional de filtros a aplicar
            
        Returns:
            Logger configurado
        """
        # Crear logger
        logger = logging.getLogger('vision_artificial')
        logger.setLevel(self.log_level)

        # Evitar duplicación de handlers
        if logger.handlers:
            return logger

        # Configurar handler para consola
        console = logging.StreamHandler()
        console.setLevel(self.log_level)

        # Configurar handler para archivo
        file_handler = logging.handlers.RotatingFileHandler(
            os.path.join(self.log_path, 'app.log'),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(self.log_level)

        # Aplicar filtros si se proporcionan
        all_filters = self.filters
        if filters:
            all_filters.extend(filters)

        for f in all_filters:
            console.addFilter(f)
            file_handler.addFilter(f)

        # Configurar formato
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Agregar handlers
        logger.addHandler(console)
        logger.addHandler(file_handler)

        # Guardar referencia global sin usar global statement
        # Use a class-level approach instead
        _set_app_logger(logger)

        return logger


def _set_app_logger(logger: logging.Logger) -> None:
    """
    Sets the application logger without using global statement.
    
    Args:
        logger: Logger to set
    """
    # Using globals() dictionary to avoid global statement
    globals()['_APP_LOGGER'] = logger


def get_logger() -> logging.Logger:
    """
    Retorna el logger global configurado.
    Si no está configurado, devuelve un logger básico.
    
    Returns:
        Logger configurado
    """
    if _APP_LOGGER is None:
        return logging.getLogger('vision_artificial')
    return _APP_LOGGER
