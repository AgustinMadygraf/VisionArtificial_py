"""
Path: src/routes/home.py
"""

from flask import Blueprint, redirect, current_app

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    # Ejemplo de acceso al contenedor DI (para futuras dependencias):
    # container = current_app.container
    return redirect('http://127.0.0.1:80/computervision')
