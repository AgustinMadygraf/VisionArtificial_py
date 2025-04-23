"""
Módulo de registro dinámico de servicios.
Permite registrar y obtener implementaciones de servicios por interfaz.
"""

_service_registry = {}

def register_service(interface, implementation):
    """
    Registra una implementación para una interfaz dada.
    Args:
        interface (str): Nombre de la interfaz.
        implementation (type): Clase de la implementación.
    """
    _service_registry[interface] = implementation

def get_service_implementation(interface):
    """
    Obtiene la implementación registrada para una interfaz.
    Args:
        interface (str): Nombre de la interfaz.
    Returns:
        type: Clase de la implementación registrada.
    Raises:
        KeyError: Si no hay implementación registrada para la interfaz.
    """
    return _service_registry[interface]
