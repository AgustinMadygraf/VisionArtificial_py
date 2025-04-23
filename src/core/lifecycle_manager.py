"""
Path: src/core/lifecycle_manager.py
Gestor de eventos de ciclo de vida de la aplicación Flask.
Permite registrar callbacks para eventos como 'startup' y 'shutdown'.
"""

class LifecycleManager:
    def __init__(self):
        self._events = {
            'startup': [],
            'shutdown': [],
        }

    def on(self, event, callback):
        if event in self._events:
            self._events[event].append(callback)
        else:
            raise ValueError(f"Evento desconocido: {event}")

    def trigger(self, event, *args, **kwargs):
        for callback in self._events.get(event, []):
            callback(*args, **kwargs)

lifecycle_manager = LifecycleManager()
