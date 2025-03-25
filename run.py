"""
Path: run.py
Archivo de entrada simplificado para iniciar la aplicación.
"""

from threading import Thread

from src.factory import create_app
from src.tkinter_view import TkinterViewer
app = create_app()

def run_flask():
    app.run(debug=True, use_reloader=False)

flask_thread = Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

viewer = TkinterViewer()
viewer.run()

if __name__ == "__main__":
    app.run(debug=True)
