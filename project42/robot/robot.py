"""Robot module"""

MOTOR_L_FORWARD_PIN = 12
MOTOR_L_BACKWARD_PIN = 16
MOTOR_R_FORWARD_PIN = 20
MOTOR_R_BACKWARD_PIN = 21
L_IR_SENSOR = 23
R_IR_SENSOR = 24
SPEED = 64 # Value between 0 and 255 -> dutycycle = 255 / SPEED

class Robot:
    """Represents the robot."""

    def __init__(self, pi):
        self.__pi = pi
        self.is_moving = False

    def __set_motor_pwm(self, ml_f, ml_b, mr_f, mr_b):
        """Sets the GPIO pins to control the motors."""

        self.__pi.set_PWM_dutycycle(MOTOR_L_FORWARD_PIN, ml_f * SPEED)
        self.__pi.set_PWM_dutycycle(MOTOR_L_BACKWARD_PIN, ml_b * SPEED)
        self.__pi.set_PWM_dutycycle(MOTOR_R_FORWARD_PIN, mr_f * SPEED)
        self.__pi.set_PWM_dutycycle(MOTOR_R_BACKWARD_PIN, mr_b * SPEED)

    def follow_line(self):
        """Follows the black line."""

        if self.__pi.read(23) == 1 and self.__pi.read(24) == 1:
            self.hold_position()
        elif self.__pi.read(23) == 1:
            self.turn_left()
        elif self.__pi.read(24) == 1:
            self.turn_right()
        else:
            self.move_forward()

    def move_forward(self):
        """Moves the robot forward."""

        self.__set_motor_pwm(1, 0, 1, 0)
        self.is_moving = True

    def move_backwards(self):
        """Moves the robot backwards."""

        self.__set_motor_pwm(0, 1, 0, 1)
        self.is_moving = True

    def hold_position(self):
        """Stops the movement of the robot."""

        self.__set_motor_pwm(0, 0, 0, 0)
        self.is_moving = False

    def turn_left(self):
        """Turns the robot left."""

        self.__set_motor_pwm(0, 1, 1, 0)
        self.is_moving = True

    def turn_right(self):
        """Turns the robot right."""

        self.__set_motor_pwm(1, 0, 0, 1)
        self.is_moving = True
