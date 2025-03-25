"""
Módulo para procesamiento de imagen.
Define funciones para modificar frames, agregando líneas verticales y horizontales en el centro.

Función principal:
  - process_frame: Recibe un frame, dibuja una línea vertical y una línea horizontal en el centro, y retorna el frame modificado.
"""

import cv2

def process_frame(frame):
    """
    Procesa la imagen añadiendo una línea vertical y una línea horizontal en el centro.
    
    Parámetros:
        frame (numpy.ndarray): La imagen a procesar.
    
    Retorna:
        numpy.ndarray: La imagen procesada.
    """
    height, width, _ = frame.shape
    # Dibujar línea vertical en el centro
    cv2.line(frame, (width // 2, 0), (width // 2, height), (0, 0, 255), 2)
    # Dibujar línea horizontal en el centro
    cv2.line(frame, (0, height // 2), (width, height // 2), (0, 0, 255), 2)
    return frame