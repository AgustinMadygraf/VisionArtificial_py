"""
Componente para formatear frames de video en formato HTTP multipart/x-mixed-replace.
"""
import cv2

class VideoHTTPFormatter:
    """
    Clase responsable de formatear frames de video para transmisión HTTP (multipart/x-mixed-replace).
    """
    def format_frame(self, frame) -> bytes:
        """
        Codifica un frame a JPEG y lo envuelve en el formato HTTP adecuado.
        Args:
            frame: Frame de video (numpy array).
        Returns:
            bytes: Frame formateado para streaming HTTP.
        """
        try:
            _, buffer = cv2.imencode('.jpg', frame)  # pylint: disable=E1101
            return (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        except cv2.error as e: # pylint: disable=E1101
            print(f"Error al formatear el frame con OpenCV: {e}")
            return b''
