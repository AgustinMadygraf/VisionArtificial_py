"""
Path: run.py
Inicio de la aplicación.
Este módulo invoca main() de src/main.py, que orquesta la inicialización y ejecución de los componentes.
"""

from src.coordinator import ApplicationCoordinator

if __name__ == "__main__":
    try:
        coordinator = ApplicationCoordinator()
        coordinator.run()
    except KeyboardInterrupt:
        print("Interrupción detectada (Ctrl+C). Cerrando aplicación...")
