"""
Path: run.py
"""

from src.main import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupción detectada (Ctrl+C). Cerrando aplicación...")
