"""Main module"""
import sys
import imutils
#import pigpio
import robot.robot as r
import robot.camera as c
import robot.animal as a



def main(*args):
    """Main entry point of the application"""

    cam = c.Camera(a.Animals.Frog, True, 600, "./test-video1.mp4")
    robo = r.Robot(pigpio.pi())

    while robo.follow_line():
        grabbed = False
        
        if cam.check_current_frame() and not grabbed:
            grabbed = True

    return

if __name__ == "__main__":
    main(*sys.argv[1:])
