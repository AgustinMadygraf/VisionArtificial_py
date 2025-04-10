"""
Path: src/routes/video.py
"""

from flask import Blueprint, Response
# from src.services.camera_service import generate_frames  # Se importa el servicio de cámara
import cv2
from src.utils.logging.simple_logger import LoggerService

# Se crea una instancia del servicio de logger
logger = LoggerService()

video_bp = Blueprint('video', __name__)

@video_bp.route('/video_original')
def video_original():
    "Ruta para el video original."
    return Response(
        generate_frames(process=False),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@video_bp.route('/video_process')
def video_process():
    "Ruta para el video procesado."
    return Response(
        generate_frames(process=True),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


def generate_frames(process=False):
    """Establece la captura de video y procesa los frames si es necesario."""
    camera_index = 0
    print(f"Intentando acceder a la cámara con índice {camera_index}.")
    camera = cv2.VideoCapture(camera_index)  # pylint: disable=no-member
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
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # pylint: disable=no-member
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)  # pylint: disable=no-member

                _, buffer = cv2.imencode('.jpg', frame)  # pylint: disable=no-member
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                _, buffer = cv2.imencode('.jpg', frame)   # pylint: disable=no-member
                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    except RuntimeError as e:
        logger.error(f"Error durante la captura de video: {e}")
    finally:
        print("Liberando la cámara.")
        camera.release()
