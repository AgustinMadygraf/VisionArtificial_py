"""
Path: src/extensions.py
Módulo para inicializar y almacenar extensiones de Flask.
"""
from flask_cors import CORS

# Instancias de extensiones (pueden agregarse más en el futuro)
cors = CORS

def init_extensions(app):
    cors(app)
    # Aquí puedes inicializar otras extensiones, por ejemplo:
    # db.init_app(app)
    # login_manager.init_app(app)
