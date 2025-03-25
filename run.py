"""
Path: run.py
Archivo de entrada simplificado para iniciar la aplicación.
"""

from src.factory import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
