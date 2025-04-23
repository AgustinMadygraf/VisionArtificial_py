"""
Buffer thread-safe para almacenar frames de video entre productor y consumidor.
"""
import queue

class FrameBuffer:
    def __init__(self, maxsize=10):
        self._queue = queue.Queue(maxsize=maxsize)

    def put(self, frame):
        try:
            self._queue.put(frame, timeout=1)
        except queue.Full:
            # Se puede loggear o manejar el overflow del buffer
            pass

    def get(self):
        try:
            return self._queue.get(timeout=1)
        except queue.Empty:
            # Se puede loggear o manejar el underflow del buffer
            return None

    def empty(self):
        return self._queue.empty()

    def full(self):
        return self._queue.full()
