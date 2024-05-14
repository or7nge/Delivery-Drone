from config import *
import numpy as np
import argparse
import time
import cv2
import sys
from aruko_processor import ArukoProcessor


class Camera:
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.aruko_processor = ArukoProcessor()

    def camera_loop(self):
        while True:
            ret, frame = self.video.read()
            print(type(frame))
            if ret is False:
                break

            self.aruko_processor.add_frame(frame)
            cv2.imshow("Image", self.aruko_processor.frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

        cv2.destroyAllWindows()
        self.video.release()


if __name__ == "__main__":
    camera = Camera()
    camera.camera_loop()
