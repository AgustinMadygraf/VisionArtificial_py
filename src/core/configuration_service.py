"""
Path: src/services/configuration_service.py
"""

import json
import os
from typing import Any, Callable, Dict, List, Optional

from src.interfaces.IConfigurationService import IConfigurationService
from src.interfaces.ILogger import ILogger
from src.utils.logging.simple_logger import LoggerService
from src.config import DEFAULT_CONFIG
from src.core.frame_processor import FrameProcessor  # Importar FrameProcessor

class ConfigurationService(IConfigurationService):
    """
    Servicio de configuración centralizado que gestiona los parámetros
    de configuración del sistema y notifica a los observadores cuando estos cambian.
    """
    
    def __init__(self, logger: Optional[ILogger] = None):
        """
        Inicializa el servicio de configuración.
        
        Args:
            logger: Servicio de logging opcional.
        """
        self._logger = logger or LoggerService()
        self._config = {}
        self._observers: List[Callable[[str, Any, Any], None]] = []
        
        # Inicializar con la configuración predeterminada
        self._initialize_default_config()
        
        self._logger.info("ConfigurationService inicializado con éxito")
    
    def _initialize_default_config(self) -> None:
        """Inicializa el servicio con la configuración por defecto."""
        # Extraemos los atributos de DEFAULT_CONFIG que no son métodos ni privados
        for key, value in DEFAULT_CONFIG.__dict__.items():
            if not key.startswith('_') and not callable(value):
                self._config[key] = value
                
        self._logger.debug(f"Configuración inicializada con: {self._config}")
    
    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Obtiene el valor de un parámetro de configuración.
        
        Args:
            key: Clave del parámetro de configuración.
            default: Valor por defecto si la clave no existe.
            
        Returns:
            El valor del parámetro o el valor por defecto si no existe.
        """
        value = self._config.get(key, default)
        self._logger.debug(f"Obteniendo configuración: {key} = {value}")
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Establece el valor de un parámetro de configuración.
        
        Args:
            key: Clave del parámetro de configuración.
            value: Nuevo valor para el parámetro.
        """
        old_value = self._config.get(key)
        self._config[key] = value
        
        # Actualizar también DEFAULT_CONFIG para mantener compatibilidad
        # mientras se migra completamente al nuevo sistema
        if hasattr(DEFAULT_CONFIG, key):
            setattr(DEFAULT_CONFIG, key, value)
        
        self._logger.info(f"Configuración actualizada: {key} = {value} (antes: {old_value})")
        
        # Notificar a los observadores
        for observer in self._observers:
            try:
                observer(key, old_value, value)
            except Exception as e:
                self._logger.error(f"Error al notificar observador: {e}")
        
        # Sincronizar con FrameProcessor si es necesario
        if key == "PIXELS_TO_UNITS" and FrameProcessor._config_service is self:
            FrameProcessor._config_service = self
    
    def get_all(self) -> Dict[str, Any]:
        """
        Obtiene todos los parámetros de configuración.
        
        Returns:
            Diccionario con todos los parámetros de configuración.
        """
        return self._config.copy()
    
    def add_observer(self, observer: Callable[[str, Any, Any], None]) -> None:
        """
        Registra un observador para ser notificado cuando cambia un parámetro.
        
        Args:
            observer: Función que será llamada con (key, old_value, new_value)
                     cuando un parámetro cambie.
        """
        if observer not in self._observers:
            self._observers.append(observer)
            self._logger.debug(f"Observador agregado: {observer}")
    
    def remove_observer(self, observer: Callable[[str, Any, Any], None]) -> None:
        """
        Elimina un observador previamente registrado.
        
        Args:
            observer: Función previamente registrada como observador.
        """
        if observer in self._observers:
            self._observers.remove(observer)
            self._logger.debug(f"Observador eliminado: {observer}")
    
    def export_to_file(self, file_path: str) -> bool:
        """
        Exporta la configuración actual a un archivo JSON.
        
        Args:
            file_path: Ruta del archivo donde se guardará la configuración.
            
        Returns:
            True si la exportación fue exitosa, False en caso contrario.
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=4)
            self._logger.info(f"Configuración exportada exitosamente a: {file_path}")
            return True
        except Exception as e:
            self._logger.error(f"Error exportando configuración: {e}")
            return False
    
    def import_from_file(self, file_path: str) -> bool:
        """
        Importa la configuración desde un archivo JSON.
        
        Args:
            file_path: Ruta del archivo desde donde se cargará la configuración.
            
        Returns:
            True si la importación fue exitosa, False en caso contrario.
        """
        if not os.path.exists(file_path):
            self._logger.error(f"El archivo no existe: {file_path}")
            return False
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                new_config = json.load(f)
            
            # Guardar configuración antigua para notificar cambios
            old_config = self._config.copy()
            
            # Actualizar configuración
            for key, value in new_config.items():
                self.set(key, value)
            
            self._logger.info(f"Configuración importada exitosamente desde: {file_path}")
            return True
        except Exception as e:
            self._logger.error(f"Error importando configuración: {e}")
            return False