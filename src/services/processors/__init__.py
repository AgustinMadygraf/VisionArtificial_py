from .grayscale_processor import GrayscaleProcessor
from .edge_detection_processor import EdgeDetectionProcessor
from .blur_processor import BlurProcessor
from .registry import processor_registry

# Registro automático de procesadores disponibles
processor_registry.register('grayscale', GrayscaleProcessor)
processor_registry.register('edge_detection', EdgeDetectionProcessor)
processor_registry.register('blur', BlurProcessor)
# Aquí puedes registrar más procesadores en el futuro
# processor_registry.register('otro', OtroProcessor)