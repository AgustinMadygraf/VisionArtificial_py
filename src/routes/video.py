"""
Path: src/routes/video.py
"""

from flask import Blueprint, Response
import cv2

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
    """Genera frames de video, procesados o no."""
    camera = cv2.VideoCapture(0)  # pylint: disable=no-member
    if not camera.isOpened():
        return

    try:
        while True:
            success, frame = camera.read()
            if not success:
                break

            if process:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # pylint: disable=no-member
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)  # pylint: disable=no-member

            _, buffer = cv2.imencode('.jpg', frame)  # pylint: disable=no-member
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    finally:
        camera.release()
        cv2.destroyAllWindows()  # pylint: disable=no-member
