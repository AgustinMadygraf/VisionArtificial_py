#VisionArtificial\src\image_processing.py
import cv2
import numpy as np
import datetime
from src.rotacion import rotar_imagen
from src.deteccion_bordes import encontrar_borde
from src.logs.config_logger import configurar_logging
from src.registro_desvios import registrar_desvio 

TOLERANCIA = 2  # Tolerancia en milímetros

# Configuración del logger
logger = configurar_logging()

def dibujar_reglas(frame, pixels_por_mm=20):
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
    int_pixels = int(pixels_por_mm)
    for mm in range(int(-centro_x / int_pixels), int(centro_x / int_pixels)):
        if mm % 10 == 0:  # Marcas más largas para centímetros
            cv2.line(frame, (centro_x + mm * int_pixels, centro_y - 10), (centro_x + mm * int_pixels, centro_y + 10), (255, 255, 255), 2)
            cv2.putText(frame, str(mm // 10), (centro_x + mm * int_pixels - 5, centro_y + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)
        else:  # Marcas más cortas para milímetros
            cv2.line(frame, (centro_x + mm * int_pixels, centro_y - 5), (centro_x + mm * int_pixels, centro_y + 5), (255, 255, 255), 1)
            cv2.putText(frame, str(mm), (centro_x + mm * int_pixels - 5, centro_y + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)

    return frame
def calcular_desvio_en_mm(posicion_borde_x, ancho_imagen, pixels_por_mm):
    centro_imagen_x = ancho_imagen / 2
    desvio_pixeles = posicion_borde_x - centro_imagen_x
    desvio_mm = desvio_pixeles / pixels_por_mm
    desvio_mm = round(desvio_mm, 2)

    return desvio_mm

class ProcessingController:
    def __init__(self, default_pixels_por_mm=20):
        self.default_pixels_por_mm = default_pixels_por_mm
        # ...existing initialization if needed...

    def process(self, frame, grados, altura, horizontal, pixels_por_mm):
        try:
            if grados != 0:
                frame = rotar_imagen(frame, grados)
            if horizontal != 0:
                frame = desplazar_horizontal(frame, horizontal)
            # Edge detection: obtener borde y la posición (max_x)
            frame, max_x = encontrar_borde(frame)
            # Dibujar reglas usando el valor de pixels_por_mm
            frame = dibujar_reglas(frame, pixels_por_mm)
            
            # Calcular desviación
            desvio_mm = calcular_desvio_en_mm(max_x, frame.shape[1], pixels_por_mm)
            
            # Obtener información de tiempo
            now = datetime.datetime.now()
            fecha_hora = now.strftime("%d-%m-%Y %H:%M:%S")
            texto0 = fecha_hora
            texto1 = registrar_desvio(desvio_mm, TOLERANCIA)
            texto2 = "Ancho de bobina: 790mm"
            texto3 = "Formato bolsa: 260x120x360"
            texto4 = "solapa: 30mm"
            
            # Posicionamiento del texto (arriba a la derecha)
            posicion0 = (frame.shape[1] - 700, 100)
            posicion1 = (frame.shape[1] - 700, 150)
            posicion2 = (frame.shape[1] - 700, 200)
            posicion3 = (frame.shape[1] - 700, 250)
            posicion4 = (frame.shape[1] - 700, 300)
            
            fuente = cv2.FONT_HERSHEY_SIMPLEX
            escala_fuente = 0.7
            color = (0, 255, 255)  # Amarillo
            grosor = 2
            
            # Dibujar textos
            cv2.putText(frame, texto0, posicion0, fuente, escala_fuente, color, grosor)
            cv2.putText(frame, texto1, posicion1, fuente, escala_fuente, color, grosor)
            cv2.putText(frame, texto2, posicion2, fuente, escala_fuente, color, grosor)
            cv2.putText(frame, texto3, posicion3, fuente, escala_fuente, color, grosor)
            cv2.putText(frame, texto4, posicion4, fuente, escala_fuente, color, grosor)
            
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
