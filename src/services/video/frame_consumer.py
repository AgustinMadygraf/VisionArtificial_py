"""
Consumidor de frames: toma frames del buffer, los procesa y los formatea para HTTP.
"""
import threading

class FrameConsumer(threading.Thread):
    def __init__(self, frame_buffer, processing_service, formatter, stop_event=None, process=False):
        super().__init__()
        self.frame_buffer = frame_buffer
        self.processing_service = processing_service
        self.formatter = formatter
        self.stop_event = stop_event or threading.Event()
        self.process = process
        self.output_queue = []  # Para almacenar frames formateados

    def run(self):
        try:
            while not self.stop_event.is_set():
                if not self.frame_buffer.empty():
                    frame = self.frame_buffer.get()
                    if frame is None:
                        continue
                    try:
                        if self.process:
                            frame = self.processing_service.process_frame(frame)
                        formatted = self.formatter.format_frame(frame)
                        self.output_queue.append(formatted)
                    except Exception as e:
                        # Loggear error de procesamiento o formateo
                        pass
        except Exception as e:
            # Loggear error general del consumidor
            pass

    def get_formatted_frame(self):
        if self.output_queue:
            return self.output_queue.pop(0)
        return None
