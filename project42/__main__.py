"""Main module"""
import sys
import imutils
#import pigpio
import robot.robot as r
import camera.camera as Camera



def main(*args):
    """Main entry point of the application"""


    Frog = Camera.Animal((29, 100, 60), (64, 255, 255), 30, "Circle")
    Tomato = Camera.Animal((0, 50, 50), (10, 255, 255), 20,"Circle")
    Rhino = Camera.Animal((90, 50, 50), (130, 255, 255), 20, "Circle")
    Leopard = Camera.Animal(,, 30, "Rectangle")

    cam = Camera.Camera(True, 600, "./test-video1.mp4")
    #cam.search_animal(Frog)
    #cam.search_animal(Tomato)
    #cam.search_animal(Rhino)

    print(args)
    robo = r.Robot(pigpio.pi())

    while True:
        robo.move_forward()

    return

if __name__ == "__main__":
    main(*sys.argv[1:])
