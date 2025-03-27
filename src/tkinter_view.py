"""
Path: src/tkinter_view.py
"""

import cv2
from tkinter import Tk, Label
from PIL import Image, ImageTk
from src.services.frame_processor import FrameProcessor
from src.services.camera_service import CameraService

class TkinterViewer:
    " Clase para crear una interfaz gráfica con Tkinter que muestra la vista de la cámara."
    def __init__(self, logger):
        self.logger = logger
        self.root = Tk()
        self.root.title("Vista Procesada")
        self.root.report_callback_exception = self.report_callback_exception
        self.label = Label(self.root)
        self.label.pack()
        self.cam = None
        self.update_frame()

    def report_callback_exception(self, exc, val, tb):
        if issubclass(exc, KeyboardInterrupt):
            self.logger.info("KeyboardInterrupt detectado en callback de Tkinter. Saliendo sin traza.")
            self.root.quit()
        else:
            self.logger.warning("Excepción no controlada en Tkinter", exc_info=(exc, val, tb))
            exit(1)

    def update_frame(self):
        try:
            if self.cam is not None:
                success, frame = self.cam.cap.read()
                if success:
                    frame = FrameProcessor.process(frame)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    im = Image.fromarray(frame)
                    imgtk = ImageTk.PhotoImage(image=im)
                    self.label.imgtk = imgtk
                    self.label.configure(image=imgtk)
            self.root.after(30, self.update_frame)
        except KeyboardInterrupt:
            self.root.quit()
        except Exception as e:
            self.logger.exception("Error en la vista tkinter")
            self.root.after(1000, self.update_frame)

    def run(self):
        self.cam_service = CameraService(self.logger)
        self.cam = self.cam_service.__enter__()
        try:
            self.root.mainloop()
        finally:
            try:
                if self.cam is not None:
                    self.cam_service.__exit__(None, None, None)
                    self.logger.info("Camera released successfully via CameraService.")
            except Exception as e:
                self.logger.exception("Error releasing camera in run()")
    
    def stop(self):
        if self.cam is not None:
            try:
                self.cam.cap.release()
                self.logger.info("Camera released in stop().")
            except Exception as e:
                self.logger.exception("Error releasing camera in stop()")
        self.root.quit()
