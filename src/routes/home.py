"""
Path: src/routes/home.py
"""

from flask import Blueprint, render_template
import jinja2

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    """Ruta principal que renderiza la plantilla HTML."""
    try:
        return render_template('index.html')
    except jinja2.exceptions.TemplateNotFound:
        return "Plantilla no encontrada", 404
    except jinja2.exceptions.TemplateError:
        return "Error en la plantilla", 500
