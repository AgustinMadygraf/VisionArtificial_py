"""
Path: src/services/camera_service.py
"""

import cv2
from src.utils.logging.simple_logger import LoggerService

logger = LoggerService()

def generate_frames(process=False):
    """Establece la captura de video y procesa los frames si es necesario."""
    camera_index = 0
    print(f"Intentando acceder a la cámara con índice {camera_index}.")
    camera = cv2.VideoCapture(camera_index) # pylint: disable=E1101
    if not camera.isOpened():
        print(
            f"No se pudo acceder a la cámara con índice {camera_index}. "
            "Verifica si está conectada y no está en uso."
        )
        return

    try:
        while True:
            success, frame = camera.read()
            if not success:
                logger.warning(
                    "No se pudo leer el frame de la cámara. "
                    "Verifica la conexión."
                )
                break

            if process:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # pylint: disable=E1101
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR) # pylint: disable=E1101
                _, buffer = cv2.imencode('.jpg', frame) # pylint: disable=E1101
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                _, buffer = cv2.imencode('.jpg', frame) # pylint: disable=E1101
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    except RuntimeError as e:
        logger.error(f"RuntimeError durante la captura de video: {e}")
    except cv2.error as e:  # pylint: disable=catching-non-exception
        logger.error(f"Error de OpenCV durante la captura de video: {e}")
    except Exception as e: # pylint: disable=broad-except
        logger.exception("Excepción inesperada durante la captura de video:")
    finally:
        print("Liberando la cámara.")
        camera.release()
        try:
            cv2.destroyAllWindows()  # pylint: disable=E1101
        except cv2.error as e: # pylint: disable=catching-non-exception
            logger.warning(f"Error al cerrar ventanas: {e}")
        logger.info("Cámara liberada y ventanas cerradas.")
