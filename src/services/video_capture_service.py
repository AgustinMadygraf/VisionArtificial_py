"""
VideoCaptureService: Handles video capture operations.
"""

import cv2

class VideoCaptureService:
    "Handles video capture from a camera."
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.camera = None

    def open_camera(self):
        "Open the camera for video capture."
        self.camera = cv2.VideoCapture(self.camera_index, cv2.CAP_ANY) # pylint: disable=E1101
        if not self.camera.isOpened():
            raise RuntimeError(f"Cannot open camera with index {self.camera_index}")

    def read_frame(self):
        "Read a frame from the camera."
        if not self.camera:
            raise RuntimeError("Camera is not opened")
        success, frame = self.camera.read()
        if not success:
            raise RuntimeError("Failed to read frame from camera")
        return frame

    def release_camera(self):
        "Release the camera resource."
        if self.camera:
            self.camera.release()
            self.camera = None
