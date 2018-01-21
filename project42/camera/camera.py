"""Camera module"""

from collections import deque
import numpy as np
import argparse
import imutils
import cv2

"""Animals"""
TURTLE = Animal((29,86,6), (64, 255, 255), 15, "Circle")

class Camera:

    def __init__(self, showImage = False, frameWidth = 600):
        self.camera = cv2.VideoCapture(0)
        self.showImage = showImage
        self.frameWidth = frameWidth
        self.calibrationIndex = 100 """used to modify colors based on surroundings??"""

    def __exit__(self, exc_type, exc_value, traceback):
        camera.release()
        cv2.destroyAllWindows()

    def search_animal(self, animal):
        found = False
        while not found:
            found = self._check_current_frame(animal.lowerColor, animal.upperColor, animal.minContourSize, animal.contourType)
        #Event/Callback-Methode...
         Return True   
        
        
    def calibrate(self):
        self.calibrationIndex = 42
        
    def _check_current_frame(self, lowerColor, upperColor, minContourSize, contourType, blur = FALSE):
        (grabbed, frame) = self.camera.read()
        if not grabbed:
            return False
        frame = imutils.resize(frame, self.frameWidth)
        if blur:
            frame = cv2.GaussianBlur(frame, (11,11),0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, lowerColor, upperColor)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            if contourType == "Circle":
                ((x,y), contourSize) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                
            elif contourType == "Rectangle":
                """do something else"""

            if contourSize > minContourSize:
                """sucessfully recognized"""
                if self.showImage:
                    """draw depending on contourType"""
                    if contourType == "Circle":
                        cv2.circle(frame, (int(x),int(y)), int(radius), (0, 255, 255),2)
                        cv2.circle(frame, center, 5, (0,0,255), -1)
                    elif contourType == "Rectangle":
                        """draw Rectangle"""
                    cv2.imshow("Frame", frame)
                Return True

        return False
    
