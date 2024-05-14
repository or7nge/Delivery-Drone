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

    def get_pixel_distance(self):
        center = self.get_center()
        distance = np.linalg.norm(center - self.drone_center)
        return distance

    def get_real_distance(self):
        return self.get_pixel_distance() / self.get_aruco_pixel_width() * REAL_ARUKO_WIDTH

    def get_drone_rotation(self):
        center = self.get_center()
        angle = np.arctan2(center[0] - self.drone_center[0], self.drone_center[1] - center[1])
        angle = np.degrees(angle)
        return angle

    def get_front_rotation(self):
        angle = np.arctan2(self.topRight[1] - self.topLeft[1], self.topRight[0] - self.topLeft[0])
        angle = np.degrees(angle)
        return angle

    def get_aruco_pixel_width(self):
        return np.linalg.norm(self.topLeft - self.topRight)

    def get_frame_real_width(self):
        return FRAME_WIDTH * REAL_ARUKO_WIDTH / self.get_pixel_size()

    def get_real_height(self):
        real_width = self.get_real_width()
        return (real_width / 2) / np.tan(np.radians(CAMERA_ANGLE / 2))
