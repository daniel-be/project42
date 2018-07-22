"""Camera module"""

import math
import numpy as np
import imutils
from imutils.video import VideoStream
import cv2

CONTOUR_TYPE_RECTANGLE = 114
CONTOUR_TYPE_CIRCLE = 99

class Camera:
    """Represents the camera."""
    def __init__(self, show_image=False, video="none"):
        if video == "none":
            self.camera = VideoStream(0, True)
        else:
            self.camera = VideoStream(video)
        
        self.camera.start()
        self.show_image = show_image

    def __exit__(self, exc_type, exc_value, traceback):
        self.camera.stop()
        cv2.destroyAllWindows()

    def set_animal(self, animal):
        self.animal = animal

    def check_current_frame(self, blur=False):
        """Checks the current frame for the animal."""
        frame = self.camera.read()
        if frame is None:
            return False

        self.frame_width = frame.shape[1]

        mask = cv2.GaussianBlur(frame, (15, 15), 0)
        mask = cv2.medianBlur(mask, 7)

        hsv = cv2.cvtColor(mask, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, self.animal.lower_color, self.animal.upper_color)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, (7, 7))

        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        if contours:
            # Get closest contour to middle
            c = self.__get_closest_contour_to_middle(contours)
            contour_size = cv2.contourArea(c)

            # Calculate center of mass
            m = cv2.moments(c)
            center = (int(m["m10"] / m["m00"]), int(m["m01"] / m["m00"]))

            if (contour_size > self.animal.min_contour_size and 
                math.fabs(center[0] - self.frame_width / 2) < self.animal.tolerance_to_middle and
                self.animal.min_contour_size * self.animal.contour_size_tolerance >= contour_size):
                #sucessfully recognized
                return True

        return False

    def __calc_distance_to_middle(self, contour):
        m = cv2.moments(contour)
        print(m)
        if  m["m00"] > 0:
            center = (int(m["m10"] / m["m00"]), int(m["m01"] / m["m00"]))
            return math.fabs(center[0] - self.frame_width / 2)
        else:
            return -1

    def __get_closest_contour_to_middle(self, contours):
        closest = None
        closest_distance = self.frame_width / 2

        for c in contours:
            distance_to_middle = self.__calc_distance_to_middle(c)

            if distance_to_middle < closest_distance and distance_to_middle >= 0:
                closest_distance = distance_to_middle
                closest = c

        return closest
