import cv2
import numpy as np
from tkinter import Tk, Label
from PIL import Image, ImageTk
from src.camera import Camera
from src.utils.logging.simple_logger import LoggerService

class TkinterViewer:
    def __init__(self):
        self.logger = LoggerService()
        self.root = Tk()
        self.root.title("Vista Procesada")
        self.label = Label(self.root)
        self.label.pack()
        # Se usa Camera() directamente para capturar frames
        self.cam = Camera().__enter__()
        self.update_frame()

    def update_frame(self):
        try:
            success, frame = self.cam.cap.read()
            if success:
                height, width, _ = frame.shape
                cv2.line(frame, (width // 2, 0), (width // 2, height), (0, 0, 255), 2)  # línea vertical roja
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                im = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=im)
                self.label.imgtk = imgtk
                self.label.configure(image=imgtk)
            self.root.after(30, self.update_frame)
        except Exception as e:
            self.logger.exception("Error en la vista tkinter")
            self.root.after(1000, self.update_frame)

    def run(self):
        self.root.mainloop()
        self.cam.__exit__(None, None, None)

if __name__ == "__main__":
    viewer = TkinterViewer()
    viewer.run()
