"""Main module"""
import sys
import imutils
import time
#import pigpio
import robot.robot as r
import robot.camera as c
import robot.animal as a
from bluetooth import *

def main(*args):
    """Main entry point of the application"""

    server_sock=BluetoothSocket( RFCOMM )
    server_sock.bind(("",PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]

    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    advertise_service( server_sock, "MarvinServer",
                    service_id = uuid,
                    service_classes = [ uuid, SERIAL_PORT_CLASS ],
                    profiles = [ SERIAL_PORT_PROFILE ])

    robo = r.Robot(pigpio.pi())

    try:
        while True:
            client_sock, client_info = server_sock.accept()
            print("Accepted connection from ", client_info)

            try:
                while True:
                    data = client_sock.recv(1024)
                    print(data)
                    '''
                    cam = c.Camera(a.Animal(data), True, 600, "../test-video1.mp4")
                    grabbed = False

                    robo.move_forward()

                    while not robo.done:
                        if cam.check_current_frame() and not grabbed:
                            robo.hold_position()
                            robo.grab()
                            grabbed = True
                            robo.move_forward()
                            
                    '''
            except IOError:
                print("Bluetooth connection was closed.")
    except:
        print("Error!")

if __name__ == "__main__":
    main(*sys.argv[1:])
