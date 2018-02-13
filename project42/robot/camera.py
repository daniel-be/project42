"""Camera module"""

import math
import numpy as np
import imutils
import cv2

class Animal:
    """Represents an animal."""
    def __init__(self, lower_color, upper_color, min_contour_size, contour_type):
        self.lower_color = lower_color
        self.upper_color = upper_color
        self.min_contour_size = min_contour_size
        self.contour_type = contour_type

class Animals():
    """no enum as base class to avoid having to use .value in selector"""
    Frog = Animal((29, 100, 60), (64, 255, 255), 30, "Rectangle")
    Tomato = Animal((0, 50, 50), (10, 255, 255), 20, "Circle")
    Rhino = Animal((90, 50, 50), (130, 255, 255), 20, "Circle")
    #Leopard = Animal((90, 50, 50), (130, 255, 255), 30, "Rectangle")

class Camera:
    """Represents the camera."""
    def __init__(self, animal, show_image=False, frame_width=600,
                 video="none", tolerance_to_middle=40):
        if video == "none":
            self.camera = cv2.VideoCapture(0)
        else:
            self.camera = cv2.VideoCapture(video, 0)
        if not self.camera.isOpened():
            print("camera not open")
        self.show_image = show_image
        self.frame_width = frame_width
        self.animal = animal
        self.tolerance_to_middle = tolerance_to_middle
        #used to modify colors based on surroundings??
        self.calibration_index = 100

    def __exit__(self, exc_type, exc_value, traceback):
        self.camera.release()
        cv2.destroyAllWindows()

    def calibrate(self):
        """Sets the calibration index."""
        self.calibration_index = 42

    def check_current_frame(self, blur=False):
        """Checks the current frame for the animal."""
        found = False
        (grabbed, frame) = self.camera.read()
        if not grabbed:
            return False
        frame = imutils.resize(frame, self.frame_width)

        if blur:
            frame = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, self.animal.lower_color, self.animal.upper_color)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        if contours:
            c = max(contours, key=cv2.contourArea)
            if self.animal.contour_type == "Circle":
                ((x, y), contour_size) = cv2.minEnclosingCircle(c)
                m = cv2.moments(c)
                center = (int(m["m10"] / m["m00"]), int(m["m01"] / m["m00"]))
            elif self.animal.contour_type == "Rectangle":
                rect = cv2.minAreaRect(c)
                contour_size = rect[1][0] * rect[1][1] #width * height
                center = (rect[0][0], rect[0][1])
            if (contour_size > self.animal.min_contour_size and
                    math.fabs(center[0] - self.frame_width / 2) < self.tolerance_to_middle):
                #sucessfully recognized
                if self.show_image:
                    if self.animal.contour_type == "Circle":
                        cv2.circle(frame, (int(x), int(y)), int(contour_size), (0, 255, 255), 2)
                        cv2.circle(frame, center, 5, (0, 0, 255), -1)
                    elif self.animal.contour_type == "Rectangle":
                        box = cv2.boxPoints(rect)
                        box = np.int0(box)
                        cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)
                found = True
        if self.show_image:
            cv2.imshow("frame", frame)
            cv2.waitKey(10)
        return found
