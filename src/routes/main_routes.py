"""
Path: src/routes/main_routes.py
"""

from flask import Blueprint, render_template
from flask import request
import os

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def home():
    return render_template("index.html")

@main_bp.route("/shutdown")
def shutdown():
    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is None:
        os._exit(0)
    shutdown_func()
    return "Servidor cerrándose..."
