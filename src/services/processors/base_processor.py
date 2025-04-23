"""
Clase base para procesadores de video.
Implementa la interfaz IVideoProcessor y puede contener funcionalidad común.
"""
from src.interfaces.i_video_processor import IVideoProcessor

class BaseVideoProcessor(IVideoProcessor):
    def __init__(self, **kwargs):
        """
        Inicializa el procesador base. Puede aceptar parámetros comunes.
        """
        pass

    def process_frame(self, frame):
        """
        Método base. Debe ser implementado por subclases.
        """
        raise NotImplementedError("Subclases deben implementar process_frame.")
