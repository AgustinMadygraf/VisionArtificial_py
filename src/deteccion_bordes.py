import numpy as np
import logging

logger = logging.getLogger(__name__)

def filtrar_por_color(image, rgb):
    """
    Filtra una imagen por color.

    Parámetros:
    - image (np.ndarray): Imagen de entrada para filtrar.
    - rgb (tuple): Valor RGB del color a filtrar.
    
    Retorna:
    - np.ndarray: Máscara binaria donde los píxeles que coinciden con el color dado son True.
    """
    try:
        color = np.array(rgb)
        diff = np.abs(image - color)
        sum_diff = np.sum(diff, axis=2)
        mask = sum_diff < 30
        return mask
    except Exception as e:
        logger.error(f"Error al filtrar por color: {e}")
        raise

def filtrar_por_rango_color(image, rgb1, rgb2):
    """
    Filtra una imagen por un rango de colores.

    Parámetros:
    - image (np.ndarray): Imagen de entrada para filtrar.
    - rgb1, rgb2 (tuple): Valores RGB de los colores a filtrar.
    
    Retorna:
    - np.ndarray: Máscara binaria donde los píxeles que están en el rango de los colores dados son True.
    """
    try:
        color1 = np.array(rgb1)
        color2 = np.array(rgb2)
        mask = np.all((image >= color1) & (image <= color2), axis=2)
        return mask
    except Exception as e:
        logger.error(f"Error al filtrar por rango de colores: {e}")
        raise

def encontrar_borde(frame):
    try:
        cols = frame.shape[1]
        start_col = int(cols * 0.2)
        end_col = int(cols * 0.8)

        # Definir el rango de colores y el color a asignar
        color1 = (200, 200, 200)  # Color inferior del rango
        color2 = (255, 255, 255)  # Color superior del rango
        color_asignado = (0, 0, 255)  # Color a asignar

        # Filtrar la imagen por el rango de colores
        mask = filtrar_por_rango_color(frame, color1, color2)

        # Asignar el color a los píxeles en el rango de colores
        frame[mask] = color_asignado

        grey_avg = calcular_promedio_gris(frame[:, start_col:end_col])
        mean = np.mean(grey_avg, axis=0).reshape(end_col - start_col)
        max_x_central = calcular_derivadas(mean).argmax()
        max_x = max_x_central + start_col
        frame[:, max_x, :] = (255, 255, 0)
        return frame, max_x  
    except Exception as e:
        logger.error(f"Error al encontrar el borde: {e}")
        raise

def calcular_promedio_gris(image):
    try:
        return np.mean(image, axis=2).reshape((*image.shape[:2], 1))
    except Exception as e:
        logger.error(f"Error al calcular el promedio de gris: {e}")
        raise

def calcular_derivadas(array):
    try:
        left, mid, right = array[:-2], array[1:-1], array[2:]
        return 2 * mid - left - right
    except Exception as e:
        logger.error(f"Error al calcular derivadas: {e}")
        raise