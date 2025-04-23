# Excepciones relacionadas con configuración
from .base import VisionArtificialError

class ConfigError(VisionArtificialError):
    """Excepción base para errores de configuración."""
    pass

class ConfigNotFoundError(ConfigError):
    """No se encontró la configuración solicitada."""
    pass

class InvalidConfigError(ConfigError):
    """La configuración es inválida o está corrupta."""
    pass
