"""Main module"""
import sys
import imutils
import time
import robot.robot as r
import robot.camera as c
import robot.animal as a

def main(*args):
    """Main entry point of the application"""
    #Animal(lower_color, upper_color, min_contour_size, contour_type, tolerance_to_middle)
    #contour_type 99 = Circle
    RHINO = a.Animal((47,51,37),(126,255,255), 0, 99, 57)
    TOMATO = a.Animal((138,72,0),(241,255,255), 0, 99, 50)
    LEOPARD = a.Animal((0,114,52),(23,227,248), 38, 99, 50)
    FROG = a.Animal((30,65,0),(91,255,77), 40, 99, 50)
    TURTLE = a.Animal((0,37,124),(14,72,197), 15, 99, 50)

    cam = c.Camera(TURTLE, True, 600, 'C:\\Users\\Sven\\Documents\\Programmieren\\Video2.mp4' )
    found = False
    try:
        while not found:
            if(cam.check_current_frame()):
                print("found!")
                #found = True
    except KeyboardInterrupt:
        print("not found")
        pass    

if __name__ == "__main__":
    main(*sys.argv[1:])
