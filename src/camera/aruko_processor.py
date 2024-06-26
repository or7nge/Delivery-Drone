from config import *
import numpy as np
from .frame_extended import FrameExtended
from .aruko_detector import OrangeArucoDetector
from .detected_aruko import DetectedAruko
from .directive import Directive


class ArukoProcessor:
    def __init__(self, queue):
        self.queue = queue
        self.aruko_detector = OrangeArucoDetector()
        self.aruko_queue = []

    def add_frame(self, frame):
        frame = FrameExtended(frame)
        aruko = self.aruko_detector.detectMarker(frame)
        self.add_aruko(aruko)
        current_directive = self.get_directive()
        self.queue.put(current_directive)
        frame.show_info(self.average_aruko, current_directive)
        return frame

    def add_aruko(self, aruko):
        self.aruko_queue.append(aruko)
        if len(self.aruko_queue) > ARUKO_QUEUE_SIZE:
            self.aruko_queue.pop(0)
        self.find_average_aruko()

    def get_directive(self):
        if not self.average_aruko:
            return Directive("NO ARUKO")

        distance = self.average_aruko.get_pixel_distance()
        drone_rotation = self.average_aruko.get_drone_rotation()
        front_rotation = self.average_aruko.get_front_rotation()
        aruco_pixel_width = self.average_aruko.get_aruco_pixel_width()

        if distance < DISTANCE_THRESHOLD:
            if aruco_pixel_width > FRAME_HEIGHT // 3 and abs(front_rotation) > FRONT_ROTATION_THRESHOLD:
                return Directive("ROTATE", int(front_rotation))
            return Directive("DESCEND")
        if abs(drone_rotation) > DRONE_ROTATION_THRESHOLD:
            return Directive("ROTATE", int(drone_rotation))
        return Directive("MOVE", int(self.average_aruko.get_real_distance()))

    def find_average_aruko(self):
        self.average_aruko = None
        aruko_queue_cleared = []
        weights = []
        for i in range(len(self.aruko_queue)):
            if self.aruko_queue[i]:
                aruko_queue_cleared.append(self.aruko_queue[i].corners)
                weights.append(i + 1)
        if not aruko_queue_cleared:
            return
        self.average_aruko = DetectedAruko(np.average(aruko_queue_cleared, axis=0, weights=weights))
