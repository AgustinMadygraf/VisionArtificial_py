"""
Path: src/tkinter_view.py
"""

import tkinter
from tkinter import Tk, Label, Scale, HORIZONTAL, Button
import cv2
from PIL import Image, ImageTk
from src.services.frame_processor import FrameProcessor
from src.services.camera_service import CameraService
from src.config import DEFAULT_CONFIG

class TkinterViewer:
    " Clase para crear una interfaz gráfica con Tkinter que muestra la vista de la cámara."
    def __init__(self, logger):
        self.logger = logger
        self.root = Tk()
        self.root.title("Vista Procesada")
        self.root.report_callback_exception = self.report_callback_exception
        self.label = Label(self.root)
        self.label.pack()
        # Reemplazo del control Scale único por un Frame con botones laterales
        control_frame = tkinter.Frame(self.root)
        control_frame.pack()
        self.decrement_btn = Button(control_frame, text="-", command=self.on_decrement)
        self.decrement_btn.pack(side="left")
        self.scale = Scale(control_frame, from_=1, to=100, orient=HORIZONTAL, label="Pixels to Units", command=self.on_scale_change)
        self.scale.set(DEFAULT_CONFIG.PIXELS_TO_UNITS)
        self.scale.pack(side="left")
        self.increment_btn = Button(control_frame, text="+", command=self.on_increment)
        self.increment_btn.pack(side="left")
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

    def on_scale_change(self, value):
        "Callback para actualizar el parámetro PIXELS_TO_UNITS en tiempo real."
        from src.config import DEFAULT_CONFIG
        try:
            DEFAULT_CONFIG.PIXELS_TO_UNITS = float(value)
            self.logger.info(f"Updated PIXELS_TO_UNITS to {DEFAULT_CONFIG.PIXELS_TO_UNITS}")
        except ValueError:
            self.logger.error("Invalid value for PIXELS_TO_UNITS")

    def on_decrement(self):
        "Callback para decrementar el valor de PIXELS_TO_UNITS."
        new_value = self.scale.get() - 1
        if new_value < self.scale['from']:
            new_value = self.scale['from']
        self.scale.set(new_value)
        self.on_scale_change(new_value)

    def on_increment(self):
        "Callback para incrementar el valor de PIXELS_TO_UNITS."
        new_value = self.scale.get() + 1
        if new_value > self.scale['to']:
            new_value = self.scale['to']
        self.scale.set(new_value)
        self.on_scale_change(new_value)

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
