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

class Animals():
    """no enum as base class to avoid having to use .value in selector"""
    Frog = Animal((29, 100, 60), (64, 255, 255), 30, "Rectangle")
    Tomato = Animal((0, 50, 50), (10, 255, 255), 20,"Circle")
    Rhino = Animal((90, 50, 50), (130, 255, 255), 20, "Circle")
    #Leopard = Animal((90, 50, 50), (130, 255, 255), 30, "Rectangle")

class Camera:
    """Camera class"""
    def __init__(self, animal,showImage = False, frameWidth = 600, video = "none"):
        if(video == "none"):
            self.camera = cv2.VideoCapture(0)
        else:
            self.camera = cv2.VideoCapture(video, 0)
        if not (self.camera.isOpened()):
            print("camera not open")
        self.showImage = showImage
        self.frameWidth = frameWidth
        self.animal = animal
        #used to modify colors based on surroundings??
        self.calibrationIndex = 100 
        

    def __exit__(self, exc_type, exc_value, traceback):
        camera.release()
        cv2.destroyAllWindows()

    def search_animal(self):
        found = False
        #while not found:
        while True:
            found = self.check_current_frame()
        #Event/Callback-Methode...
        return True
        
        
    def calibrate(self):
        self.calibrationIndex = 42
        
    def check_current_frame(self, blur = False):
        found = False
        (grabbed, frame) = self.camera.read()
        if not grabbed:
            return False
        frame = imutils.resize(frame, self.frameWidth)

        if blur:
            frame = cv2.GaussianBlur(frame, (11,11),0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, self.animal.lowerColor, self.animal.upperColor)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            if self.animal.contourType == "Circle":
                ((x,y), contourSize) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            elif self.animal.contourType == "Rectangle":
                rect = cv2.minAreaRect(c)
                contourSize = rect[1][0] * rect[1][1] #width * height
            if contourSize > self.animal.minContourSize:
                #sucessfully recognized
                if self.showImage:
                    if self.animal.contourType == "Circle":
                        cv2.circle(frame, (int(x),int(y)), int(contourSize), (0, 255, 255),2)
                        cv2.circle(frame, center, 5, (0,0,255), -1)
                    elif self.animal.contourType == "Rectangle":
                        box = cv2.boxPoints(rect)
                        box = np.int0(box)
                        cv2.drawContours(frame,[box],0,(0,0,255),2)
                found = True
        if self.showImage:
            cv2.imshow("frame", frame)
            cv2.waitKey(10)
        return found
    

