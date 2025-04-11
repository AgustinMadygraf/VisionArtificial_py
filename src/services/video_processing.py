"""
VideoProcessingService: Handles frame processing operations.
"""

import cv2

class VideoProcessingService:
    "Handles video frame processing."
    @staticmethod
    def process_frame(frame):
        """Apply transformations to the frame."""
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # pylint: disable=E1101
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR) # pylint: disable=E1101
        height, width, _ = frame.shape
        # Draw a red vertical line in the center
        cv2.line(frame, (width // 2, 0), (width // 2, height), (0, 0, 255), 2) # pylint: disable=E1101
        # Draw a blue horizontal line in the center
        cv2.line(frame, (0, height // 2), (width, height // 2), (255, 0, 0), 2) # pylint: disable=E1101
        return frame
