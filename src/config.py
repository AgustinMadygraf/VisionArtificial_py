"""
Path: src/config.py
"""

class AppConfig:
    "Clase de configuración para la aplicación."
    def __init__(self, template_folder="../templates", static_folder="../static", pixels_to_units=10):
        self.TEMPLATE_FOLDER = template_folder
        self.STATIC_FOLDER = static_folder
        self.PIXELS_TO_UNITS = pixels_to_units

DEBUG = True

# Agregado: instancia por defecto para configuración global
DEFAULT_CONFIG = AppConfig()
# Nota: DEFAULT_CONFIG.PIXELS_TO_UNITS ahora es el parámetro centralizado y se puede modificar en tiempo real desde la interfaz Tkinter.
