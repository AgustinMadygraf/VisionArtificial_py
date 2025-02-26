#VisionArtificial\config_manager.py
import json
import os
import sys
from src.logs.config_logger import configurar_logging

# Configuración del logger
logger = configurar_logging()
def leer_configuracion(config_path):
    """
    Lee la configuración desde el archivo 'config.json' y devuelve un diccionario con los valores configurados.
    Si el archivo no existe, se crea uno con valores predeterminados.
    """
    config_path = 'src/config.json'
    configuracion_predeterminada = {
        "grados_rotacion_default": 0.0,
        "horizontal_default": 0.0,
        "altura_default": 0.0,
        "url_default": "192.168.0.119",
        "ubicacion_default": "C:/AppServ/www/VisionArtificial_py/tests/calibracion_deteccion_papel.jpg",
        "pixels_por_mm_default": 35
    }

    try:
        if not os.path.exists(config_path):
            with open(config_path, 'w') as archivo:
                json.dump(configuracion_predeterminada, archivo, indent=4)
            logger.info("Archivo de configuración creado con valores predeterminados.")

        with open(config_path, 'r') as archivo:
            datos = json.load(archivo)
    except Exception as e:
        logger.error(f"Error al leer o crear el archivo de configuración: {e}")
        sys.exit(1)
    
    return datos

def actualizar_configuracion(config_path, nueva_config):
    """
    Actualiza el archivo config.json con la nueva configuración proporcionada.

    Parámetros:
    - config_path (str): Ruta al archivo config.json.
    - nueva_config (dict): Diccionario con los valores de configuración actualizados.
    """
    try:
        with open(config_path, 'r+') as archivo:
            config = json.load(archivo)
            config.update(nueva_config)
            archivo.seek(0)  # Regresa al inicio del archivo para sobrescribir
            json.dump(config, archivo, indent=4)
            archivo.truncate()  # Trunca el archivo al tamaño actual, en caso de que el nuevo contenido sea más corto
    except Exception as e:
        logger.error(f"Error al actualizar la configuración: {e}")
