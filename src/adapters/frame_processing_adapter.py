from src.core.frame_processor import FrameProcessor

class FrameProcessingAdapter:
    """
    Adapter to centralize frame processing logic for different interfaces.
    """
    @staticmethod
    def process_frame(frame):
        return FrameProcessor.process(frame)