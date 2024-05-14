from config import *
import cv2
from detected_aruko import DetectedAruko


class OrangeArucoDetector(cv2.aruco.ArucoDetector):
    def __init__(self):
        self.dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
        self.parameters = cv2.aruco.DetectorParameters()
        super().__init__(self.dictionary, self.parameters)

    def detectMarker(self, image):
        (corners, ids, rejected) = self.detectMarkers(image)
        if not corners:
            return None
        ids = ids.flatten()
        for corners, markerID in zip(corners, ids):
            if markerID != 69:
                continue
            return DetectedAruko(corners[0])
