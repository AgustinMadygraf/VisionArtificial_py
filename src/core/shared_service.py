from src.interfaces.service_interface import IService
from src.core.camera_service import CameraService
from src.core.frame_processor import FrameProcessor

class SharedService(IService):
    """
    Clase que centraliza el acceso a servicios compartidos.
    """

    def __init__(self, logger):
        self.logger = logger
        self.camera_service = CameraService(logger)
        self.frame_processor = FrameProcessor
        self.camera = None  # Inicializar el atributo camera como None

    def initialize(self):
        """
        Inicializa los servicios compartidos.
        """
        self.logger.info("Inicializando servicios compartidos.")
        self.camera = self.camera_service.__enter__()  # Guardar referencia al objeto Camera

    def shutdown(self):
        """
        Finaliza los servicios compartidos.
        """
        self.logger.info("Finalizando servicios compartidos.")
        self.camera_service.__exit__(None, None, None)

    def get_camera_service(self):
        """
        Devuelve el objeto Camera.
        """
        return self.camera  # Devolver el objeto Camera

    def get_frame_processor(self):
        """
        Devuelve el procesador de frames.
        """
        return self.frame_processor
