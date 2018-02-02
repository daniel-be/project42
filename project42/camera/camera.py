"""Camera module"""

from collections import deque
import numpy as np
import argparse
import imutils
import cv2

class Animal:
    """animal class"""
    def __init__(self, lowerColor, upperColor, minContourSize, contourType):
        self.lowerColor = lowerColor
        self.upperColor = upperColor
        self.minContourSize = minContourSize
        self.contourType = contourType

TURTLE = Animal((87,43,26), (110, 40, 20), 15, "Circle")

class Camera:
    """Camera class"""

    def __init__(self, showImage = False, frameWidth = 600, video = "none"):
        if(video == "none"):
            self.camera = cv2.VideoCapture(0)
        else:
            self.camera = cv2.VideoCapture(video, 0)
        if not (self.camera.isOpened()):
            print("camera not open")
        self.showImage = showImage
        self.frameWidth = frameWidth
        #used to modify colors based on surroundings??
        self.calibrationIndex = 100 

    def __exit__(self, exc_type, exc_value, traceback):
        camera.release()
        cv2.destroyAllWindows()

    def search_animal(self, animal):
        found = False
        #while not found:
        while True:
            found = self._check_current_frame(animal.lowerColor, animal.upperColor, animal.minContourSize, animal.contourType)
        #Event/Callback-Methode...
        return True
        
        
    def calibrate(self):
        self.calibrationIndex = 42
        
    def _check_current_frame(self, lowerColor, upperColor, minContourSize, contourType, blur = False):
        found = False
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
                #do something else
                print("Rectangle")
            if contourSize > minContourSize:
                #sucessfully recognized
                if self.showImage:
                    #draw depending on contourType
                    if contourType == "Circle":
                        cv2.circle(frame, (int(x),int(y)), int(contourSize), (0, 255, 255),2)
                        cv2.circle(frame, center, 5, (0,0,255), -1)
                    elif contourType == "Rectangle":
                        #draw Rectangle
                        print("Rectangle again!")
                found = True
        if self.showImage:
            cv2.imshow("frame", frame)
            cv2.waitKey(10)
        return found
    

