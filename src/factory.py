"""
Path: src/factory.py
"""

from flask import Flask
from src.routes.main_routes import main_bp
from src.routes.video_routes import video_bp

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.register_blueprint(main_bp)
    app.register_blueprint(video_bp)
    return app
