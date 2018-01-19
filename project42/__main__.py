"""Main module"""
import sys
import pigpio
import robot.robot as r

def main(*args):
    """Main entry point of the application"""
    print(args)
    robo = r.Robot(pigpio.pi())

    while True:
        robo.move_forward()

    return

if __name__ == "__main__":
    main(*sys.argv[1:])
