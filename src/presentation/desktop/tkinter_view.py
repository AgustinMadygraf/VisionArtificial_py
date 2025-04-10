"""
Path: src/tkinter_view.py
"""

import tkinter
from tkinter import Tk, Label, Scale, HORIZONTAL, Button
# Suppress type-checking errors for cv2 members
import cv2  # type: ignore
from PIL import Image, ImageTk
from src.config import DEFAULT_CONFIG
from src.adapters.tkinter_adapter import TkinterAdapter
from src.core.shared_service import SharedService
from src.presentation.desktop.camera_controller import CameraController
from src.presentation.desktop.config_controller import ConfigController

class ConfigChangeObserver:
    def __init__(self, callback):
        self.callback = callback

    def on_config_change(self, key, old_value, new_value):
        """Callback method to handle configuration changes."""
        self.callback(key, old_value, new_value)

class TkinterViewer:
    "Clase para crear una interfaz gráfica con Tkinter que muestra la vista de la cámara."
    def __init__(self, logger, config_service=None):
        self.logger = logger
        self.config_service = config_service
        self.shared_service = SharedService(logger)  # Usar SharedService
        self.adapter = TkinterAdapter(logger)
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
        self.scale = Scale(
            control_frame,
            from_=1,
            to=100,
            orient=HORIZONTAL,
            label="Pixels to Units",
            command=self.on_scale_change
        )
        
        # Obtener la configuración inicial del servicio si está disponible,
        # o usar DEFAULT_CONFIG como respaldo
        if self.config_service:
            initial_value = self.config_service.get("PIXELS_TO_UNITS", DEFAULT_CONFIG.PIXELS_TO_UNITS)
        else:
            initial_value = DEFAULT_CONFIG.PIXELS_TO_UNITS
            
        self.scale.set(initial_value)
        self.scale.pack(side="left")
        self.increment_btn = Button(control_frame, text="+", command=self.on_increment)
        self.increment_btn.pack(side="left")
        self.camera_controller = CameraController(self.shared_service)  # Delegar a CameraController
        self.config_controller = ConfigController(config_service)  # Delegar a ConfigController
        self.config_controller.add_observer(ConfigChangeObserver(self.on_config_change))
        self.update_frame()

    def report_callback_exception(self, exc, val, tb):
        "Maneja excepciones no controladas en Tkinter."
        if issubclass(exc, KeyboardInterrupt):
            self.logger.info(
                "KeyboardInterrupt detectado en callback de Tkinter. "
                "Cerrando aplicación..."
            )
            self.root.quit()
        else:
            self.logger.exception("Excepción no controlada en Tkinter", exc_info=(exc, val, tb))
            self.stop()
            
    def on_config_change(self, key, _, new_value):
        "Callback llamado cuando cambia un valor en el servicio de configuración."
        if key == "PIXELS_TO_UNITS" and self.scale.get() != new_value:
            self.logger.debug(f"Actualizando UI por cambio en configuración: {key}={new_value}")
            self.scale.set(new_value)

    def update_frame(self):
        "Actualiza el frame de la cámara en la interfaz gráfica."
        try:
            frame = self.camera_controller.get_frame()  # Delegar a CameraController
            if frame is not None:
                frame = self.shared_service.get_frame_processor().process(frame)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # type: ignore[attr-defined, no-member]
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
        try:
            value_float = float(value)
            
            # Actualizar exclusivamente mediante el servicio de configuración
            if self.config_service:
                self.config_service.set("PIXELS_TO_UNITS", value_float)
            else:
                self.logger.error("ConfigurationService no está disponible.")
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
        self.shared_service.initialize()  # Inicializar servicios compartidos
        try:
            self.root.mainloop()
        finally:
            self.logger.info("Cerrando servicios compartidos.")
            self.shared_service.shutdown()  # Finalizar servicios compartidos

    def stop(self):
        "Detiene la interfaz gráfica y libera los recursos de la cámara."
        self.camera_controller.shutdown()  # Delegar a CameraController
        self.shared_service.shutdown()  # Usar SharedService
        self.root.quit()
        try:
            self.root.destroy()
        except tkinter.TclError as e:
            self.logger.exception("Error destroying Tkinter root window", exc_info=e)
