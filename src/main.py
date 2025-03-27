"""
Path: src/main.py
"""

import argparse
from threading import Thread
from src.factory import create_app
from src.tkinter_view import TkinterViewer

def run_server():
    app = create_app()
    app.run(debug=True, use_reloader=False)

def run_gui():
    viewer = TkinterViewer()
    viewer.run()

def main():
    parser = argparse.ArgumentParser(description="Ejecutar componentes de la aplicación")
    parser.add_argument('--mode', choices=['flask', 'tkinter', 'both'], default='both', 
                        help="Modo de ejecución: 'flask', 'tkinter' o 'both' (por defecto ambos)")
    args = parser.parse_args()

    flask_thread = None
    if args.mode == 'flask':
        run_server()
    elif args.mode == 'tkinter':
        run_gui()
    elif args.mode == 'both':
        flask_thread = Thread(target=run_server)
        flask_thread.daemon = True
        flask_thread.start()
        run_gui()
        flask_thread.join(timeout=1)
