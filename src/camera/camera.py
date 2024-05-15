from config import *
import cv2
from .aruko_processor import ArukoProcessor


class Camera:
    def __init__(self, queue):
        self.queue = queue
        self.video = cv2.VideoCapture(0)
        self.aruko_processor = ArukoProcessor(self.queue)

    def cut_frame(self, frame):
        global FRAME_HEIGHT, FRAME_WIDTH
        FRAME_HEIGHT = FRAME_WIDTH = min(frame.shape[:2])
        height, width, _ = frame.shape
        min_dim = min(height, width)
        start_x = (width - min_dim) // 2
        start_y = (height - min_dim) // 2
        frame = frame[start_y: start_y + min_dim, start_x: start_x + min_dim]
        return frame

    def camera_loop(self):
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (480, 480))
        while True:
            ret, frame = self.video.read()
            frame = self.cut_frame(frame)
            if ret is False:
                break

            extended_frame = self.aruko_processor.add_frame(frame)

            # Write the extended_frame to the video file
            out.write(extended_frame)

            cv2.imshow("Image", extended_frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

        cv2.destroyAllWindows()
        self.video.release()


def start_camera_loop(queue):
    camera = Camera(queue)
    camera.camera_loop()
