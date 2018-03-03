"""Camera module"""

import math
import numpy as np
import imutils
import cv2

class Camera:
    """Represents the camera."""
    def __init__(self, animal, show_image=False, frame_width=600,
                 video="none"):
        if video == "none":
            self.camera = cv2.VideoCapture(0)
        else:
            self.camera = cv2.VideoCapture(video, 0)
        if not self.camera.isOpened():
            print("camera not open")
        self.show_image = show_image
        self.frame_width = frame_width
        self.animal = animal
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
                    math.fabs(center[0] - self.frame_width / 2) < self.animal.tolerance_to_middle):
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
