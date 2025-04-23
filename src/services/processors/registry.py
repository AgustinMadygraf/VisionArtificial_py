"""
Registro de procesadores de video disponibles.
Permite registrar y obtener procesadores por nombre.
"""
from typing import Dict, Type
from src.interfaces.i_video_processor import IVideoProcessor

class ProcessorRegistry:
    def __init__(self):
        self._registry: Dict[str, Type[IVideoProcessor]] = {}

    def register(self, name: str, processor_cls: Type[IVideoProcessor]):
        self._registry[name] = processor_cls

    def get(self, name: str) -> Type[IVideoProcessor]:
        if name not in self._registry:
            raise ValueError(f"Procesador '{name}' no registrado.")
        return self._registry[name]

    def available(self):
        return list(self._registry.keys())

processor_registry = ProcessorRegistry()
