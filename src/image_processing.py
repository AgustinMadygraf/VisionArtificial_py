#VisionArtificial\src\image_processing.py
import cv2
import numpy as np
from rotacion import rotar_imagen
from deteccion_bordes import encontrar_borde
from logs.config_logger import configurar_logging

# Configuración del logger
logger = configurar_logging()

def dibujar_reglas(frame, pixels_por_mm=10):
    """
    Dibuja una línea horizontal y una línea vertical centradas en la imagen, con una regla sobre la línea
    horizontal que marca milímetros y centímetros. La línea vertical es roja, de 1 pixel de grosor y punteada.

    Parámetros:
    - frame (np.ndarray): Imagen en la que se dibujarán las líneas y marcas de la regla.
    - pixels_por_mm (int): Número de píxeles que representan un milímetro en la imagen.

    Retorna:
    - np.ndarray: La imagen con una línea horizontal y una vertical dibujadas, y una regla sobre la horizontal.
    """
    altura, ancho = frame.shape[:2]
    centro_x, centro_y = ancho // 2, altura // 2

    # Dibujar línea horizontal verde
    cv2.line(frame, (0, centro_y), (ancho, centro_y), (0, 255, 0), 2)

    # Dibujar línea vertical roja y punteada
    for y in range(0, altura, 4):  # Cambia 4 por otro valor para ajustar el espaciado de los puntos
        if y % 8 < 4:  # Cambia 4 para ajustar la longitud de los segmentos
            cv2.line(frame, (centro_x, y), (centro_x, min(y+2, altura)), (255, 0, 0), 1)  # Cambia 2 para ajustar la longitud de los segmentos

    # Dibujar marcas de milímetros y números de centímetros
    for mm in range(-centro_x // pixels_por_mm, centro_x // pixels_por_mm):
        if mm % 10 == 0:  # Marcas más largas para centímetros
            cv2.line(frame, (centro_x + mm * pixels_por_mm, centro_y - 10), (centro_x + mm * pixels_por_mm, centro_y + 10), (255, 255, 255), 2)
            cv2.putText(frame, str(mm // 10), (centro_x + mm * pixels_por_mm - 5, centro_y + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)
        else:  # Marcas más cortas para milímetros
            cv2.line(frame, (centro_x + mm * pixels_por_mm, centro_y - 5), (centro_x + mm * pixels_por_mm, centro_y + 5), (255, 255, 255), 1)

    return frame

def process_image(frame, grados, altura, horizontal):
    """
    Procesa la imagen aplicando rotación, desplazamiento horizontal, corrección de perspectiva y detección de bordes.
    """
    try:
        # Rotación de la imagen si se especifica un ángulo diferente de cero
        if grados != 0:
            frame = rotar_imagen(frame, grados)
        
        # Desplazamiento horizontal
        if horizontal != 0:
            frame = desplazar_horizontal(frame, horizontal)
        
        # Detección de bordes y dibujo de reglas
        frame = encontrar_borde(frame)
        frame = dibujar_reglas(frame)

        return frame
    except Exception as e:
        logger.error(f"Error al procesar la imagen: {e}")
        raise

def desplazar_horizontal(frame, horizontal):
    """
    Desplaza la imagen horizontalmente según el valor especificado.

    Parámetros:
    - frame (np.ndarray): La imagen a desplazar.
    - horizontal (float): La cantidad de desplazamiento horizontal.
    
    Retorna:
    - np.ndarray: La imagen desplazada.
    """
    altura, ancho = frame.shape[:2]
    M = np.float32([[1, 0, horizontal], [0, 1, 0]])  # Matriz de transformación
    return cv2.warpAffine(frame, M, (ancho, altura))
