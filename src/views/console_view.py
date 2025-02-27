"""
Vista para manejar interacciones de consola con el usuario.
Implementa la capa de presentación del patrón MVC.
"""

import logging
from typing import Dict, Any, Tuple, Optional

class ConsoleView:
    """Clase responsable de la interacción con el usuario vía consola."""
    
    def __init__(self, logger: logging.Logger):
        """
        Inicializa la vista de consola.
        
        Args:
            logger: Logger configurado para registrar eventos
        """
        self.logger = logger
    
    def mostrar_menu_fuente_video(self) -> str:
        """
        Muestra el menú de opciones de fuente de video y captura la elección del usuario.
        
        Returns:
            La opción seleccionada por el usuario
        """
        return input(
            "Seleccione una opción:\n"
            "0 - Testing\n"
            "1 - RTSP\n"
            "2 - HTTP\n"
            "3 - Cámara web\n"
            "Opción: "
        ) or "3"
    
    def solicitar_parametros_usuario(self, config: Dict[str, Any]) -> Dict[str, float]:
        """
        Solicita y recoge los parámetros del usuario vía consola.
        
        Args:
            config: Diccionario con valores por defecto para mostrar al usuario
            
        Returns:
            Diccionario con los valores ingresados por el usuario
        """
        grados_rotacion = input(
            f'Ingrese los grados de rotación (valor por defecto "{config["grados_rotacion_default"]}"): '
        ) or str(config["grados_rotacion_default"])
        
        pixels_por_mm = input(
            f'Ingrese el valor de pixeles por mm (valor por defecto "{config["pixels_por_mm_default"]}"): '
        ) or str(config["pixels_por_mm_default"])
        
        altura = input(
            f'Ingrese la altura para corregir eje vertical (valor por defecto "{config["altura_default"]}"): '
        ) or str(config["altura_default"])
        
        horizontal = input(
            f'Ingrese el desplazamiento horizontal (valor por defecto "{config["horizontal_default"]}"): '
        ) or str(config["horizontal_default"])
        
        # Retornamos un diccionario con los valores ingresados
        return {
            'grados_rotacion': float(grados_rotacion),
            'pixels_por_mm': float(pixels_por_mm),
            'altura': float(altura),
            'horizontal': float(horizontal)
        }
    
    def mostrar_error(self, mensaje: str) -> None:
        """
        Muestra un mensaje de error al usuario.
        
        Args:
            mensaje: Mensaje de error a mostrar
        """
        print(f"ERROR: {mensaje}")
        self.logger.error(mensaje)
    
    def mostrar_info(self, mensaje: str) -> None:
        """
        Muestra un mensaje informativo al usuario.
        
        Args:
            mensaje: Mensaje informativo a mostrar
        """
        print(f"INFO: {mensaje}")
        self.logger.info(mensaje)
