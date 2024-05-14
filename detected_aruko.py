from config import *
import numpy as np
import argparse
import time
import cv2
import sys


class DetectedAruko:
    def __init__(self, corners):
        self.corners = corners
        self.drone_center = np.array([FRAME_WIDTH // 2, FRAME_HEIGHT // 2])
        self.topLeft = corners[0]
        self.topRight = corners[1]
        self.bottomRight = corners[2]
        self.bottomLeft = corners[3]

    def get_center(self):
        return np.mean(self.corners, axis=0)

    def get_distance(self):
        center = self.get_center()
        distance = np.linalg.norm(center - self.drone_center)
        return distance

    def get_drone_rotation(self):
        center = self.get_center()
        angle = np.arctan2(center[0] - self.drone_center[0], self.drone_center[1] - center[1])
        angle = np.degrees(angle)
        return angle

    def get_front_rotation(self):
        angle = np.arctan2(self.corners[1][1] - self.corners[0][1], self.corners[1][0] - self.corners[0][0])
        angle = np.degrees(angle)
        return angle

    def get_size(self):
        return np.linalg.norm(self.corners[0] - self.corners[1])

    def get_height(self):
        print(self.get_size())
        real_width = REAL_ARUKO_WIDTH * FRAME_WIDTH / self.get_size()
        height = (real_width / 2) / np.tan(np.radians(CAMERA_ANGLE / 2))
        return height

    def get_action(self):
        distance = self.get_distance()
        drone_rotation = self.get_drone_rotation()
        front_rotation = self.get_front_rotation()
        size = self.get_size()

        if distance < DISTANCE_THRESHOLD:
            if size > SIZE_THRESHOLD and abs(front_rotation) > FRONT_ROTATION_THRESHOLD:
                return f"ROTATE {int(front_rotation)}"
            return "DESCEND"
        if abs(drone_rotation) > DRONE_ROTATION_THRESHOLD:
            return f"ROTATE {int(drone_rotation)}"
        return f"MOVE {int(distance)}"
