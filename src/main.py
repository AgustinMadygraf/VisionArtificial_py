"""
Path: src/main.py
"""

import cv2
from flask import Flask, Response, render_template
import jinja2

class MainApp:
    "Clase principal de la aplicación Flask."
    def __init__(self, logger):
        self.logger = logger
        self.app = Flask(__name__, template_folder="../templates")
        self.setup_routes()

    def setup_routes(self):
        "Configuración de las rutas de la aplicación Flask."

        @self.app.route('/')
        def home():
            "Ruta principal que renderiza la plantilla HTML."
            self.logger.info("Accediendo a la ruta principal.")
            try:
                ruta_principal = render_template('index.html')
                self.logger.debug("Plantilla 'index.html' renderizada correctamente.")
                return ruta_principal
            except jinja2.exceptions.TemplateNotFound as e:
                self.logger.error(f"Plantilla 'index.html' no encontrada: {e}")
                return "Plantilla no encontrada", 404
            except jinja2.exceptions.TemplateError as e:
                self.logger.error(f"Error en la plantilla 'index.html': {e}")
                return "Error en la plantilla", 500

        @self.app.route('/video_original')
        def video_original():
            return Response(
                self.generate_frames(process=False),
                mimetype='multipart/x-mixed-replace; boundary=frame'
            )

        @self.app.route('/video_process')
        def video_process():
            return Response(
                self.generate_frames(process=True),
                mimetype='multipart/x-mixed-replace; boundary=frame'
            )

    def generate_frames(self, process=False):
        """Establece la captura de video y procesa los frames si es necesario."""
        camera_index = 0  # Cambia este índice si tienes múltiples cámaras
        self.logger.info(f"Intentando acceder a la cámara con índice {camera_index}.")
        camera = cv2.VideoCapture(camera_index)  # pylint: disable=no-member
        if not camera.isOpened():
            self.logger.error(
                f"No se pudo acceder a la cámara con índice {camera_index}. "
                "Verifica si está conectada y no está en uso."
            )
            return

        try:
            while True:
                success, frame = camera.read()
                if not success:
                    self.logger.warning(
                        "No se pudo leer el frame de la cámara. "
                        "Verifica la conexión."
                    )
                    break

                if process:
                    self.logger.debug("Procesando frame en escala de grises.")
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # pylint: disable=no-member
                    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)  # pylint: disable=no-member

                    _, buffer = cv2.imencode('.jpg', frame)  # pylint: disable=no-member
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                else:
                    self.logger.debug("No se procesará el frame.")
                    _, buffer = cv2.imencode('.jpg', frame)   # pylint: disable=no-member
                    yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

        except RuntimeError as e:
            self.logger.error(f"Error durante la captura de video: {e}")
        finally:
            self.logger.info("Liberando la cámara.")
            camera.release()

    def run(self):
        " Inicia la aplicación Flask."
        self.logger.info("Aplicación iniciada.")
        self.app.run(debug=True)
