"""
Path: src/routes/main_routes.py
"""

import logging
from flask import Blueprint, render_template, request

main_bp = Blueprint('main', __name__)

# Assign a logger to the Blueprint
main_bp.logger = logging.getLogger("main_routes")

@main_bp.route("/")
def home():
    " Ruta principal de la aplicación."
    return render_template("index.html")

@main_bp.route("/shutdown", methods=["GET"])
def shutdown():
    " Ruta para apagar el servidor Flask."
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        main_bp.logger.error("Shutdown function not available. Ensure the app is running in development mode.")
        return "Shutdown not available", 400
    func()
    return "Server shutting down..."
