"""
Path: src/interfaces/IConfigurationService.py
"""

import abc
from typing import Any, Callable, Dict, List, Optional

class IConfigurationService(abc.ABC):
    """
    Interfaz para el servicio de configuración.
    Define el contrato para gestionar la configuración centralizada del sistema,
    permitiendo obtener, establecer y observar cambios en los parámetros de configuración.
    """
    
    @abc.abstractmethod
    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Obtiene el valor de un parámetro de configuración.
        
        Args:
            key: Clave del parámetro de configuración.
            default: Valor por defecto si la clave no existe.
            
        Returns:
            El valor del parámetro o el valor por defecto si no existe.
        """
        pass
    
    @abc.abstractmethod
    def set(self, key: str, value: Any) -> None:
        """
        Establece el valor de un parámetro de configuración.
        
        Args:
            key: Clave del parámetro de configuración.
            value: Nuevo valor para el parámetro.
        """
        pass
    
    @abc.abstractmethod
    def get_all(self) -> Dict[str, Any]:
        """
        Obtiene todos los parámetros de configuración.
        
        Returns:
            Diccionario con todos los parámetros de configuración.
        """
        pass
    
    @abc.abstractmethod
    def add_observer(self, observer: Callable[[str, Any, Any], None]) -> None:
        """
        Registra un observador para ser notificado cuando cambia un parámetro.
        
        Args:
            observer: Función que será llamada con (key, old_value, new_value)
                     cuando un parámetro cambie.
        """
        pass
    
    @abc.abstractmethod
    def remove_observer(self, observer: Callable[[str, Any, Any], None]) -> None:
        """
        Elimina un observador previamente registrado.
        
        Args:
            observer: Función previamente registrada como observador.
        """
        pass
    
    @abc.abstractmethod
    def export_to_file(self, file_path: str) -> bool:
        """
        Exporta la configuración actual a un archivo.
        
        Args:
            file_path: Ruta del archivo donde se guardará la configuración.
            
        Returns:
            True si la exportación fue exitosa, False en caso contrario.
        """
        pass
    
    @abc.abstractmethod
    def import_from_file(self, file_path: str) -> bool:
        """
        Importa la configuración desde un archivo.
        
        Args:
            file_path: Ruta del archivo desde donde se cargará la configuración.
            
        Returns:
            True si la importación fue exitosa, False en caso contrario.
        """
        pass