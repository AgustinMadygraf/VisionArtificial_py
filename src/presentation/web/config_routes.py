"""
Path: src/routes/config_routes.py
"""

from flask import Blueprint, request, jsonify
from src.core.configuration_service import ConfigurationService
from src.utils.logging.simple_logger import LoggerService
from src.core.shared_service import SharedService

config_bp = Blueprint('config', __name__, url_prefix='/config')

def get_logger():
    "Función para obtener el logger."
    return getattr(config_bp, 'logger', None) or LoggerService()

shared_service = SharedService(get_logger())  # Instanciar SharedService

def get_config_service():
    "Función para obtener el servicio de configuración."
    return getattr(config_bp, 'config_service', None) or ConfigurationService(get_logger())

@config_bp.route("", methods=["GET"])
def get_all_config():
    "Endpoint para obtener toda la configuración del sistema."
    config_service = get_config_service()
    logger = get_logger()
    logger.info("Obteniendo toda la configuración")
    
    config_data = config_service.get_all()
    return jsonify(config_data)

@config_bp.route("/<key>", methods=["GET"])
def get_config(key):
    "Endpoint para obtener un valor específico de configuración."
    config_service = get_config_service()
    logger = get_logger()
    logger.info(f"Obteniendo configuración: {key}")
    
    value = config_service.get(key)
    if value is None:
        return jsonify({"error": f"La configuración '{key}' no existe"}), 404
    
    return jsonify({key: value})

@config_bp.route("", methods=["POST"])
def update_config():
    "Endpoint para actualizar uno o varios valores de configuración."
    config_service = get_config_service()
    logger = get_logger()
    
    if not request.is_json:
        return jsonify({"error": "La solicitud debe ser JSON"}), 400
    
    data = request.get_json()
    
    if not isinstance(data, dict):
        return jsonify({"error": "El formato debe ser un objeto JSON"}), 400
    
    logger.info(f"Actualizando configuración: {data}")
    
    for key, value in data.items():
        config_service.set(key, value)
    
    return jsonify({"message": "Configuración actualizada correctamente"})

@config_bp.route("/<key>", methods=["POST"])
def update_single_config(key):
    "Endpoint para actualizar un valor específico de configuración."
    config_service = get_config_service()
    logger = get_logger()
    
    if not request.is_json:
        return jsonify({"error": "La solicitud debe ser JSON"}), 400
    
    data = request.get_json()
    
    if 'value' not in data:
        return jsonify({"error": "El campo 'value' es requerido"}), 400
    
    value = data['value']
    logger.info(f"Actualizando configuración: {key} = {value}")
    
    config_service.set(key, value)
    
    return jsonify({"message": f"Configuración '{key}' actualizada correctamente"})

@config_bp.route("/export", methods=["POST"])
def export_config():
    "Endpoint para exportar la configuración a un archivo."
    config_service = get_config_service()
    logger = get_logger()
    
    if not request.is_json:
        return jsonify({"error": "La solicitud debe ser JSON"}), 400
    
    data = request.get_json()
    
    if 'file_path' not in data:
        return jsonify({"error": "El campo 'file_path' es requerido"}), 400
    
    file_path = data['file_path']
    logger.info(f"Exportando configuración a: {file_path}")
    
    success = config_service.export_to_file(file_path)
    
    if success:
        return jsonify({"message": "Configuración exportada correctamente"})
    else:
        return jsonify({"error": "Error al exportar la configuración"}), 500

@config_bp.route("/import", methods=["POST"])
def import_config():
    "Endpoint para importar la configuración desde un archivo."
    config_service = get_config_service()
    logger = get_logger()
    
    if not request.is_json:
        return jsonify({"error": "La solicitud debe ser JSON"}), 400
    
    data = request.get_json()
    
    if 'file_path' not in data:
        return jsonify({"error": "El campo 'file_path' es requerido"}), 400
    
    file_path = data['file_path']
    logger.info(f"Importando configuración desde: {file_path}")
    
    success = config_service.import_from_file(file_path)
    
    if success:
        return jsonify({"message": "Configuración importada correctamente"})
    else:
        return jsonify({"error": "Error al importar la configuración"}), 500

@config_bp.route("/update", methods=["POST"])
def update_dynamic_config():
    """
    Endpoint para actualizar la configuración desde controles dinámicos.
    """
    logger = get_logger()
    config_service = get_config_service()

    if not request.is_json:
        return jsonify({"error": "La solicitud debe ser JSON"}), 400

    data = request.get_json()
    logger.info(f"Actualizando configuración dinámica: {data}")

    for key, value in data.items():
        config_service.set(key, value)

    return jsonify({"message": "Configuración dinámica actualizada correctamente"})