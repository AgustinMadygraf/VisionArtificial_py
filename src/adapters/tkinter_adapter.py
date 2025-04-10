from src.core.frame_processor import FrameProcessor
from src.core.camera_service import CameraService

class TkinterAdapter:
    """
    Adapter to abstract interactions between TkinterViewer and shared services.
    """
    def __init__(self, logger):
        self.logger = logger
        self.camera_service = CameraService(logger)

    def process_frame(self, frame):
        "Process a frame using the FrameProcessor."
        return FrameProcessor.process(frame)

    def get_camera_service(self):
        "Provide access to the CameraService."
        return self.camera_service