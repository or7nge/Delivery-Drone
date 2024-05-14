from config import *
import numpy as np
import argparse
import time
import cv2
import sys
from frame_extended import FrameExtended
from aruko_detector import OrangeArucoDetector


class ArukoProcessor:
    def __init__(self):
        self.aruko_detector = OrangeArucoDetector()
        self.aruko_queue = []

    def add_frame(self, frame):
        frame = FrameExtended(frame)
        aruko = self.aruko_detector.detectMarker(frame)

    def add_aruko(self):
        return
