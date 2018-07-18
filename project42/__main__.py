"""Main module"""
import sys
import imutils
import time
import pigpio
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

    pi = pigpio.pi()

    try:
        while True:
            client_sock, client_info = server_sock.accept()
            print("Accepted connection from ", client_info)

            try:
                while True:
                    data = client_sock.recv(1024)
                    animal = a.Animal(data)
                    cam = c.Camera(animal, False)
                    robo = r.Robot(pi)
                    hsv_string = "L(H" + str(animal.lower_color[0]) + "|S" + str(animal.lower_color[1]) + "|V" + str(animal.lower_color[2]) ") H(H" + str(animal.upper_color[0]) + "|S" + str(animal.upper_color[1]) + "|V" + str(animal.upper_color[2]) + ")"
                    client_sock.send("Started. Searching animal (" + hsv_string + ") ...")
                    robo.move_forward()

                    while not robo.done:
                        if cam.check_current_frame() and not robo.grabbed:
                            robo.hold_position()
                            client_sock.send("Animal found. Grabbing ...")
                            robo.grab()
                            client_sock.send("Grabbed animal. Moving to target area and unloading animal ...")
                            robo.move_forward()

                    res = ""
                    if robo.grabbed: 
                        res = "Done."
                    else:
                        res = "Animal not found. Done."

                    client_sock.send(res)

            except IOError:
                print("Bluetooth connection was closed.")
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

if __name__ == "__main__":
    main(*sys.argv[1:])
