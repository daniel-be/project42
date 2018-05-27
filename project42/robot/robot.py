"""Robot module"""
import time

MOTOR_L_FORWARD_PIN = 16
MOTOR_L_BACKWARD_PIN = 20
MOTOR_R_FORWARD_PIN = 21
MOTOR_R_BACKWARD_PIN = 26
MOTOR_GRAB_IN = 12
MOTOR_GRAB_OUT = 13
GRAB_IN_SENSOR = 17
GRAB_OUT_SENSOR = 27
L_IR_SENSOR = 23
R_IR_SENSOR = 24
PWM_FREQUENCY = 40000

class Robot:
    """Represents the robot."""

    def __init__(self, pi):
        self.__pi = pi
        self.is_moving = False
        self.l_ir_sensor_val = 0
        self.r_ir_sensor_val = 0
        self.l_ir_low_callback = None
        self.r_ir_low_callback = None
        self.l_ir_high_callback = None
        self.r_ir_high_callback = None
        self.done = False

        # Init PWM
        self.MOTOR_SPEED = 150
        self.GRAB_SPEED = 100000
        self.init_pwm()

        # Init IR sensors
        self.init_ir_sensors()

    def init_pwm(self):
        """Initializes the PWM on GPIO pins."""

        self.__pi.set_PWM_frequency(MOTOR_L_FORWARD_PIN, PWM_FREQUENCY)
        self.__pi.set_PWM_frequency(MOTOR_L_BACKWARD_PIN, PWM_FREQUENCY)
        self.__pi.set_PWM_frequency(MOTOR_R_FORWARD_PIN, PWM_FREQUENCY)
        self.__pi.set_PWM_frequency(MOTOR_R_BACKWARD_PIN, PWM_FREQUENCY)

    def destroy_ir_sensors(self):
        """Removes the interrupts for following the line."""

        self.__destory_callback(self.l_ir_low_callback)
        self.__destory_callback(self.r_ir_low_callback)
        self.__destory_callback(self.l_ir_high_callback)
        self.__destory_callback(self.r_ir_high_callback)

    def __destory_callback(self, cb):
        if cb is not None:
            cb.cancel()

    def init_ir_sensors(self):
        """Initializes the interrupts to follow the black line."""

        self.__pi.set_pull_up_down(L_IR_SENSOR, 1)
        self.__pi.set_pull_up_down(R_IR_SENSOR, 1)
        self.l_ir_low_callback = self.__pi.callback(L_IR_SENSOR, 0, self.__l_ir_interrupt)
        self.r_ir_low_callback = self.__pi.callback(R_IR_SENSOR, 0, self.__r_ir_interrupt)
        self.l_ir_high_callback = self.__pi.callback(L_IR_SENSOR, 1, self.__l_ir_interrupt)
        self.r_ir_high_callback = self.__pi.callback(R_IR_SENSOR, 1, self.__r_ir_interrupt)


    def __l_ir_interrupt(self, gpio, level, tick):
        """Turns the robot left."""

        if level == 0:
            self.move_forward()
            self.l_ir_sensor_val = 0
            self.is_moving = True
        elif level == 1:
            if self.r_ir_sensor_val == 1:
                self.unload_animal()
            else:
                self.turn_left()
                self.l_ir_sensor_val = 1
                self.is_moving = True

    def __r_ir_interrupt(self, gpio, level, tick):
        """Turns the robot right."""

        if level == 0:
            self.move_forward()
            self.r_ir_sensor_val = 0
            self.is_moving = True
        elif level == 1:
            if self.l_ir_sensor_val == 1:
                self.unload_animal()
            else:
                self.turn_right()
                self.r_ir_sensor_val = 1
                self.is_moving = True

    def __set_pwm(self, pin, val, speed):
        """Sets the GPIO pins using PWM."""

        self.__pi.set_PWM_dutycycle(pin, val * speed)

    def __set_hardware_pwm(self, pin, val, speed):
        """Sets the GPIO pins using hardware PWM."""

        self.__pi.hardware_PWM(pin, PWM_FREQUENCY, val * speed)

    def __move(self, l_forward, l_back, r_forward, r_back, l_speed_factor = 1, r_speed_factor = 1):
        """Sets the pins to move the robot in a direction."""

        self.__set_pwm(MOTOR_L_FORWARD_PIN, l_forward, self.MOTOR_SPEED * l_speed_factor)
        self.__set_pwm(MOTOR_L_BACKWARD_PIN, l_back, self.MOTOR_SPEED * l_speed_factor)
        self.__set_pwm(MOTOR_R_FORWARD_PIN, r_forward, self.MOTOR_SPEED * r_speed_factor)
        self.__set_pwm(MOTOR_R_BACKWARD_PIN, r_back, self.MOTOR_SPEED * r_speed_factor)

    def __move_grab(self, grab_in, grab_out):
        """Sets the pins to move the grab in or out."""

        self.__set_hardware_pwm(MOTOR_GRAB_IN, grab_in, self.GRAB_SPEED)
        self.__set_hardware_pwm(MOTOR_GRAB_OUT, grab_out, self.GRAB_SPEED)

    def set_motor_speed(self, speed):
        """Sets the motor speed."""

        if speed > 255 or speed < 0:
            raise ValueError("Motor speed must be between 0 and 255.")

        self.MOTOR_SPEED = speed

    def set_grab_speed(self, speed):
        """Sets the grab speed."""

        if speed > 1000000 or speed < 0:
            raise ValueError("Grab speed must be between 0 and 1000000.")

        self.GRAB_SPEED = speed

    def move_forward(self):
        """Moves the robot forward."""

        self.__move(1, 0, 1, 0)
        self.is_moving = True

    def move_backwards(self):
        """Moves the robot backwards."""

        self.__move(0, 1, 0, 1)
        self.is_moving = True

    def hold_position(self):
        """Stops the movement of the robot."""

        self.__move(0, 0, 0, 0)
        self.is_moving = False

    def turn_right(self):
        """Turns the robot right."""

        self.__move(1, 0, 0, 1)
        self.is_moving = True

    def move_right(self):
        """Moves the robot right."""

        self.__move(1, 0, 0, 1, 1, 0.6)
        self.is_moving = True

    def turn_left(self):
        """Turns the robot left."""

        self.__move(0, 1, 1, 0)
        self.is_moving = True

    def move_left(self):
        """Moves the robot left."""

        self.__move(0, 1, 1, 0, 0.6)
        self.is_moving = True

    def move_grab_in(self):
        """Moves the grab in."""

        while self.__pi.read(GRAB_IN_SENSOR) != 1:
            self.__move_grab(1, 0)

        self.__move_grab(0, 0)

    def move_grab_out(self):
        """Moves the grab out."""

        while self.__pi.read(GRAB_OUT_SENSOR) != 1:
            self.__move_grab(0, 1)

        self.__move_grab(0, 0)

    def grab(self):
        """Grabs the animal by moving out and in the grab."""

        self.move_grab_out()
        self.move_grab_in()

    def unload_animal(self):
        """Unloads the animal."""

        self.hold_position()
        self.done = True
