from config import *
import numpy as np


class DetectedAruko:
    def __init__(self, corners):
        self.corners = corners
        self.drone_center = np.array([FRAME_WIDTH // 2, FRAME_HEIGHT // 2])
        self.topLeft = tuple(map(int, self.corners[0]))
        self.topRight = tuple(map(int, self.corners[1]))
        self.bottomRight = tuple(map(int, self.corners[2]))
        self.bottomLeft = tuple(map(int, self.corners[3]))

    def get_center(self):
        return tuple(map(int, np.mean(self.corners, axis=0)))

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
        real_width = REAL_ARUKO_WIDTH * FRAME_WIDTH / self.get_size()
        height = (real_width / 2) / np.tan(np.radians(CAMERA_ANGLE / 2))
        return height
