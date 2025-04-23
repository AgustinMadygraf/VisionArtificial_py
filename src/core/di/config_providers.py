"""
Providers para exponer configuración dinámica (SERVICES_CONFIG, VIDEO_CONFIG, etc.) al contenedor DI.
"""
from dependency_injector import providers
from src.config.config_loader import load_config

class ConfigProviders:
    config = providers.Singleton(load_config)
    services_config = providers.Callable(lambda: ConfigProviders.config().SERVICES_CONFIG)
    video_config = providers.Callable(lambda: ConfigProviders.config().VIDEO_CONFIG)
    # Agrega aquí más providers para otros parámetros de configuración si es necesario
