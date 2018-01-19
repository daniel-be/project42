"""Robot module"""

MOTOR_L_FORWARD_PIN = 4
MOTOR_L_BACKWARD_PIN = 27
MOTOR_R_FORWARD_PIN = 17
MOTOR_R_BACKWARD_PIN = 22

class Robot:
    """Represents the robot."""

    def __init__(self, pi):
        self.__pi = pi
        self.is_moving = False

    def __set_motor_pins(self, ml_f, ml_b, mr_f, mr_b):
        """Sets the GPIO pins to control the motors."""

        self.__pi.write(MOTOR_L_FORWARD_PIN, ml_f)
        self.__pi.write(MOTOR_L_BACKWARD_PIN, ml_b)
        self.__pi.write(MOTOR_R_FORWARD_PIN, mr_f)
        self.__pi.write(MOTOR_R_BACKWARD_PIN, mr_b)

    def move_forward(self):
        """Moves the robot forward."""

        self.__set_motor_pins(1, 0, 1, 0)
        self.is_moving = True

    def move_backwards(self):
        """Moves the robot backwards."""

        self.__set_motor_pins(0, 1, 0, 1)
        self.is_moving = True

    def hold_position(self):
        """Stops the movement of the robot."""

        self.__set_motor_pins(0, 0, 0, 0)
        self.is_moving = False

    def turn_left(self):
        """Turns the robot left."""

        self.__set_motor_pins(0, 1, 1, 0)
        self.is_moving = True

    def turn_right(self):
        """Turns the robot right."""

        self.__set_motor_pins(1, 0, 0, 1)
        self.is_moving = True