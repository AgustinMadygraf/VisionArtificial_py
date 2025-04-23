"""
Módulo de Factoría de Servicios

Este módulo centraliza la creación de instancias de servicios,
facilitando la inyección de dependencias y mejorando la modularidad.
"""

from src.services.video_capture_service import VideoCaptureService
from src.services.video_processing import VideoProcessingService
from src.core.service_registry import get_service_implementation

# Nuevo: Permitir configuración externa para la selección de implementaciones
_factory_config = {
    'video_capture_service': VideoCaptureService,
    'video_processing_service': VideoProcessingService,
}

# Diccionario para almacenar instancias singleton
_singleton_instances = {}

# Configuración de modo singleton por servicio
_singleton_config = {
    'video_capture_service': False,  # Por defecto, no singleton
    'video_processing_service': False,
}

# Diccionario para almacenar parámetros de inicialización de servicios
_service_params = {}

def configure_factory(config_dict):
    """
    Permite configurar la factory con un diccionario que mapea nombres de servicios a clases.
    Args:
        config_dict (dict): Diccionario con claves 'video_capture_service',
        'video_processing_service', etc.
    """
    _factory_config.update(config_dict)

def configure_singletons(singleton_dict):
    """
    Permite configurar qué servicios deben comportarse como singleton.
    Args:
        singleton_dict (dict): Diccionario con claves de servicio y valores booleanos.
    """
    _singleton_config.update(singleton_dict)

def configure_service_params(params_dict):
    """
    Permite configurar los parámetros de inicialización de los servicios.
    Args:
        params_dict (dict): Diccionario con claves de servicio y valores dict de parámetros.
    """
    _service_params.update(params_dict)

def get_video_capture_service():
    """
    Devuelve una instancia de la implementación configurada para VideoCaptureService.
    Primero intenta obtener la implementación del registro dinámico,
    si no existe usa la configuración local.

    Returns:
        VideoCaptureService: Instancia del servicio de captura de video.
    """
    try:
        impl = get_service_implementation('video_capture_service')
    except KeyError:
        impl = _factory_config['video_capture_service']

    params = _service_params.get('video_capture_service', {})
    if _singleton_config.get('video_capture_service', False):
        if 'video_capture_service' not in _singleton_instances:
            _singleton_instances['video_capture_service'] = impl(**params)
        return _singleton_instances['video_capture_service']

    return impl(**params)

def get_video_processing_service():
    """
    Devuelve una instancia de la implementación configurada para VideoProcessingService.
    Primero intenta obtener la implementación del registro dinámico,
    si no existe usa la configuración local.

    Returns:
        VideoProcessingService: Instancia del servicio de procesamiento de video.
    """
    try:
        impl = get_service_implementation('video_processing_service')
    except KeyError:
        impl = _factory_config['video_processing_service']

    params = _service_params.get('video_processing_service', {})
    if _singleton_config.get('video_processing_service', False):
        if 'video_processing_service' not in _singleton_instances:
            _singleton_instances['video_processing_service'] = impl(**params)
        return _singleton_instances['video_processing_service']

    return impl(**params)
