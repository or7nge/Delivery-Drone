from config import *
import numpy as np
import argparse
import time
import cv2
import sys
from aruko_detector import OrangeArucoDetector


class FrameExtended(np.ndarray):
    def __new__(cls, input_array):
        obj = np.asarray(input_array).view(cls)
        return obj

    def __init__(self):
        self.cut_frame()

    def cut_frame(self):
        height, width, _ = self.shape
        min_dim = min(height, width)
        start_x = (width - min_dim) // 2
        start_y = (height - min_dim) // 2
        self = self[start_y: start_y + min_dim, start_x: start_x + min_dim]

    def show_info(self):
        if self.aruko is None:
            return

        # draw the outline of the ArUco marker
        cv2.line(self.frame, self.aruko.topLeft, self.aruko.topRight, (0, 0, 255), 2)

        # draw the corners of the ArUco marker
        cv2.circle(self.frame, self.aruko.topLeft, 6, (255, 0, 0), -1)
        cv2.circle(self.frame, self.aruko.topRight, 6, (255, 0, 0), -1)
        cv2.circle(self.frame, self.aruko.bottomRight, 6, (255, 0, 0), -1)
        cv2.circle(self.frame, self.aruko.bottomLeft, 6, (255, 0, 0), -1)
        cv2.circle(self.frame, self.aruko.center(), 6, (255, 0, 0), -1)

        cv2.putText(self.frame, f"DRONE ROTATION: {self.drone_rotation}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(self.frame, f"DRONE HEIGHT: {self.height}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # atcion info
        if self.action == "DESCEND":
            action_color = (0, 255, 0)
        else:
            action_color = (0, 0, 255)
        cv2.circle(self.frame, (FRAME_WIDTH // 2, FRAME_HEIGHT // 2), DISTANCE_THRESHOLD, action_color, 2)
        self.updateAction(self.frame, self.action, action_color)

    def updateAction(self, text, color):
        text_width, text_height = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        text_x = FRAME_WIDTH // 2 - text_width // 2
        text_y = FRAME_HEIGHT // 2 - DISTANCE_THRESHOLD - 20 - text_height // 2
        cv2.putText(self.frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
