"""
Path: src/tkinter_view.py
"""

import cv2
import numpy as np
from tkinter import Tk, Label
from PIL import Image, ImageTk
from src.camera import Camera
from src.utils.logging.simple_logger import get_logger_instance
from src.image_processing import process_frame

class TkinterViewer:
    def __init__(self):
        self.logger = get_logger_instance()
        self.root = Tk()
        self.root.title("Vista Procesada")
        self.label = Label(self.root)
        self.label.pack()
        self.cam = None
        self.update_frame()

    def update_frame(self):
        try:
            if self.cam is not None:
                success, frame = self.cam.cap.read()
                if success:
                    frame = process_frame(frame)  # Se utiliza el procesamiento centralizado
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
        with Camera() as cam:
            self.cam = cam
            self.root.mainloop()
