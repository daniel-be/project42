"""Main module"""
import sys
import imutils
#import pigpio
import robot.robot as r
import robot.camera as Camera



def main(*args):
    """Main entry point of the application"""

    cam = Camera.Camera(Camera.Animals.Frog, True, 600, "./test-video1.mp4")
    while True:
        cam.check_current_frame()

    print(args)
    robo = r.Robot(pigpio.pi())

    while True:
        robo.move_forward()

    return

if __name__ == "__main__":
    main(*sys.argv[1:])
