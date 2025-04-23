"""
Path: src/main.py
"""

from flask import Flask
import importlib
import pkgutil
import os
from src.config.default import DefaultConfig
from src.extensions import init_extensions
from src.core.lifecycle_manager import lifecycle_manager
from src import routes

def configure_app(app, config_object):
    " Configura la aplicación Flask con el objeto de configuración proporcionado."
    app.config.from_object(config_object)

def init_extensions_wrapper(app):
    " Inicializa las extensiones de Flask."
    init_extensions(app)

def register_blueprints(app):
    """
    Descubre e importa automáticamente todos los blueprints en src.routes 
    y los registra en la app.
    Se consideran blueprints las variables que terminan en '_bp'.
    """
    package_path = os.path.dirname(routes.__file__)
    for _, module_name, is_pkg in pkgutil.iter_modules([package_path]):
        if is_pkg or module_name == "__init__":
            continue
        module = importlib.import_module(f"src.routes.{module_name}")
        for attr in dir(module):
            if attr.endswith('_bp'):
                blueprint = getattr(module, attr)
                app.register_blueprint(blueprint)

def create_flask_app(config_object=None):
    """
    Función factory para crear y configurar la aplicación Flask, con inicialización por etapas.
    """
    if config_object is None:
        config_object = DefaultConfig
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    configure_app(app, config_object)
    init_extensions_wrapper(app)
    register_blueprints(app)
    return app

class MainApp:
    "Clase principal de la aplicación Flask, usando composición."
    def __init__(self, logger, config_object=None):
        self.logger = logger
        self.config_object = config_object or DefaultConfig
        self.app = create_flask_app(self.config_object)

    def run(self, **kwargs):
        "Inicia la aplicación Flask."
        self.logger.info("Aplicación iniciada.")
        lifecycle_manager.trigger('startup', app=self.app)
        try:
            self.app.run(**kwargs)
        finally:
            lifecycle_manager.trigger('shutdown', app=self.app)
