"""
Path: src/routes/main_routes.py
"""

from flask import Blueprint, render_template, request

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def home():
    " Ruta principal de la aplicación."
    return render_template("index.html")

@main_bp.route("/shutdown", methods=["GET"])
def shutdown():
    " Ruta para apagar el servidor Flask."
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        # En lugar de finalizar abruptamente, se retorna un error controlado.
        return "Shutdown not available", 400
    func()
    return "Server shutting down..."
