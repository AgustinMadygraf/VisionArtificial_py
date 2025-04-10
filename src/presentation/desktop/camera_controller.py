from src.core.shared_service import SharedService

class CameraController:
    """
    Controlador para manejar la lógica de la cámara.
    """

    def __init__(self, shared_service: SharedService):
        self.shared_service = shared_service
        self.camera = None

    def initialize_camera(self):
        """
        Inicializa el servicio de cámara.
        """
        self.shared_service.initialize()
        self.camera = self.shared_service.get_camera_service()

    def release_camera(self):
        """
        Libera el servicio de cámara.
        """
        self.shared_service.shutdown()

    def get_frame(self):
        """
        Obtiene un frame de la cámara.
        """
        if self.camera:
            success, frame = self.camera.cap.read()
            if success:
                return frame
        return None

    def shutdown(self):
        """Releases the camera resources."""
        self.release_camera()
