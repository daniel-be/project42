import struct

"""Animal module"""

class Animal:

    """Represents an animal."""
    def __init__(self, lower_color, upper_color, min_contour_size, contour_type, tolerance_to_middle):
        self.lower_color = lower_color
        self.upper_color = upper_color
        self.min_contour_size = min_contour_size
        self.contour_type = contour_type
        self.tolerance_to_middle = tolerance_to_middle

    def init__(self, config_data):
        self.lower_color = (self.__byte_to_int(config_data[0]), self.__byte_to_int(config_data[1]), self.__byte_to_int(config_data[2]))
        self.upper_color = (self.__byte_to_int(config_data[3]), self.__byte_to_int(config_data[4]), self.__byte_to_int(config_data[5]))
        self.min_contour_size = self.__byte_to_int(config_data[6])
        self.contour_type = self.__byte_to_int(config_data[7])
        self.tolerance_to_middle = self.__byte_to_int(config_data[8])

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __byte_to_int(self, byte):
        return struct.unpack("<i", byte + "\x00\x00\x00")[0]