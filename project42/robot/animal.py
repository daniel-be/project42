"""Animal module"""

class Animal:
    """Represents an animal."""
    def __init__(self, config_data):
        self.lower_color = (int.from_bytes(config_data[0], byteorder='big'), int.from_bytes(config_data[1], byteorder='big'), int.from_bytes(config_data[2], byteorder='big'))
        self.upper_color = (int.from_bytes(config_data[3], byteorder='big'), int.from_bytes(config_data[4], byteorder='big'), int.from_bytes(config_data[5], byteorder='big'))
        self.min_contour_size = int.from_bytes(config_data[6], byteorder='big')
        self.contour_type = int.from_bytes(config_data[7], byteorder='big')
        self.tolerance_to_middle = int.from_bytes(config_data[8], byteorder='big')

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)