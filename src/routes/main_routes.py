"""
Path: src/routes/main_routes.py
"""

from flask import Blueprint, render_template, request
import sys

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def home():
    return render_template("index.html")

@main_bp.route("/shutdown", methods=["GET"])
def shutdown():
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        sys.exit("Shutdown not available. Exiting.")
    func()
    return "Server shutting down..."
