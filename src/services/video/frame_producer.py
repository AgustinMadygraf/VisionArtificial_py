"""
Productor de frames: captura frames de la cámara y los coloca en el buffer.
"""
import threading
import time

class FrameProducer(threading.Thread):
    def __init__(self, capture_service, frame_buffer, stop_event=None, fps=30):
        super().__init__()
        self.capture_service = capture_service
        self.frame_buffer = frame_buffer
        self.stop_event = stop_event or threading.Event()
        self.fps = fps

    def run(self):
        try:
            with self.capture_service:
                while not self.stop_event.is_set():
                    frame = self.capture_service.read_frame()
                    if not self.frame_buffer.full():
                        self.frame_buffer.put(frame)
                    time.sleep(1 / self.fps)
        except Exception as e:
            # Aquí se puede loggear el error de captura
            pass
