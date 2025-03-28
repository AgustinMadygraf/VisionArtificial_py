"""
Path: src/tkinter_view.py
"""

import tkinter
from tkinter import Tk, Label
import cv2
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
        self.cam_service = None
        self.update_frame()

    def report_callback_exception(self, exc, val, tb):
        "Maneja excepciones no controladas en Tkinter."
        if issubclass(exc, KeyboardInterrupt):
            self.logger.info("KeyboardInterrupt detectado en callback de Tkinter. Cerrando aplicación...")
            self.root.quit()
        else:
            self.logger.exception("Excepción no controlada en Tkinter", exc_info=(exc, val, tb))
            # Realizar cierre controlado en caso de excepciones críticas
            self.stop()

    def update_frame(self):
        "Actualiza el frame de la cámara en la interfaz gráfica."
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
        except RuntimeError:
            self.logger.exception("RuntimeError en la vista tkinter")
            self.root.after(1000, self.update_frame)

    def run(self):
        "Inicia la interfaz gráfica de Tkinter y el servicio de cámara."
        self.cam_service = CameraService(self.logger)
        with self.cam_service as cam:
            self.cam = cam
            try:
                self.root.mainloop()
            finally:
                self.logger.info("Camera released successfully via CameraService.")

    def stop(self):
        " Detiene la interfaz gráfica y libera los recursos de la cámara."
        if hasattr(self, 'cam_service'):
            self.cam_service.__exit__(None, None, None)
            self.logger.info("Camera released in stop() via CameraService.")
        else:
            if self.cam is not None:
                try:
                    self.cam.cap.release()
                    self.logger.info("Camera released in stop().")
                except RuntimeError:
                    self.logger.exception("RuntimeError occurred while releasing camera in stop()")
        self.root.quit()
        try:
            self.root.destroy()
        except tkinter.TclError as e:
            self.logger.exception("Error destroying Tkinter root window", exc_info=e)
