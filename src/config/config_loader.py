"""
Path: src/config/config_loader.py
"""

import os
from src.config.production import ProductionConfig
from src.config.default import DefaultConfig


def load_config():
    """
    Carga la clase de configuración adecuada según la variable de entorno APP_ENV.
    Valores posibles: 'default', 'production'.
    Retorna la instancia de configuración correspondiente.
    """
    env = os.environ.get('APP_ENV', 'default').lower()
    if env == 'production':
        config_class = ProductionConfig
    else:
        config_class = DefaultConfig

    # Crear una subclase dinámica para sobrescribir con variables de entorno
    class EnvConfig(config_class):
        " Configuración dinámica basada en variables de entorno. "
        # No additional implementation needed here

    # Sobrescribir atributos de configuración con variables de entorno si existen
    for key in dir(config_class):
        if key.isupper() and key in os.environ:
            val = os.environ[key]
            # Intentar convertir a tipo original si es posible
            orig_val = getattr(config_class, key)
            if isinstance(orig_val, bool):
                val = val.lower() in ('1', 'true', 'yes')
            elif isinstance(orig_val, int):
                try:
                    val = int(val)
                except ValueError:
                    pass
            setattr(EnvConfig, key, val)

    return EnvConfig()  # Retornar instancia, no clase
