from config import *
import numpy as np
import cv2
from .directive import Directive


class FrameExtended(np.ndarray):
    def __new__(cls, input_array, *args, **kwargs):
        obj = np.asarray(input_array).view(cls)
        return obj

    def __init__(self, input_array):
        return

    def show_info(self, aruko=None, directive=Directive("NO ARUKO")):
        if aruko:
            # draw the outline of the ArUco marker
            cv2.line(self, aruko.topLeft, aruko.topRight, (0, 0, 255), 2)

            # draw the corners of the ArUco marker
            cv2.circle(self, aruko.topLeft, 6, (255, 0, 0), -1)
            cv2.circle(self, aruko.topRight, 6, (255, 0, 0), -1)
            cv2.circle(self, aruko.bottomRight, 6, (255, 0, 0), -1)
            cv2.circle(self, aruko.bottomLeft, 6, (255, 0, 0), -1)
            cv2.circle(self, aruko.get_center(), 6, (255, 0, 0), -1)

            cv2.putText(self, f"DRONE ROTATION: {round(aruko.get_drone_rotation(), 2)}",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            cv2.putText(self, f"DRONE HEIGHT: {round(aruko.get_real_height(), 2)}",
                        (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        # atcion info
        cv2.circle(self, (FRAME_WIDTH // 2, FRAME_HEIGHT // 2), DISTANCE_THRESHOLD, directive.color(), 2)
        self.update_directive(str(directive), directive.color())

    def update_directive(self, text, color):
        text_width, text_height = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
        text_x = FRAME_WIDTH // 2 - text_width // 2
        text_y = FRAME_HEIGHT // 2 - DISTANCE_THRESHOLD - 10 - text_height // 2
        cv2.putText(self, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
