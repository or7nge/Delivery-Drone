from config import *
import cv2
from aruko_processor import ArukoProcessor


class Camera:
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.aruko_processor = ArukoProcessor()

    def cut_frame(self, frame):
        FRAME_HEIGHT = FRAME_WIDTH = min(frame.shape[:2])
        SIZE_THRESHOLD = FRAME_HEIGHT // 3
        height, width, _ = frame.shape
        min_dim = min(height, width)
        start_x = (width - min_dim) // 2
        start_y = (height - min_dim) // 2
        frame = frame[start_y: start_y + min_dim, start_x: start_x + min_dim]
        return frame

    def camera_loop(self):
        while True:
            ret, frame = self.video.read()
            frame = self.cut_frame(frame)
            cv2.imshow("Image", frame)
            if ret is False:
                print("Error reading frame")
                break

            extended_frame = self.aruko_processor.add_frame(frame)
            cv2.imshow("Image", extended_frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                print("Quitting")
                break

        cv2.destroyAllWindows()
        self.video.release()
