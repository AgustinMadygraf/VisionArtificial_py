# Excepciones relacionadas con servicios
from .base import VisionArtificialError

class ServiceError(VisionArtificialError):
    """Excepción base para errores de servicios."""
    pass

class ServiceUnavailableError(ServiceError):
    """Servicio no disponible o caído."""
    pass

class ServiceTimeoutError(ServiceError):
    """Timeout al acceder a un servicio."""
    pass
