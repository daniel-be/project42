"""Animal module"""

class Animal:
    """Represents an animal."""
    def __init__(self, config_data):
        self.lower_color = (int.from_bytes(config_data[0]), int.from_bytes(config_data[1]), int.from_bytes(config_data[2]))
        self.upper_color = (int.from_bytes(config_data[3]), int.from_bytes(config_data[4]), int.from_bytes(config_data[5]))
        self.min_contour_size = int.from_bytes(config_data[6])
        self.contour_type = int.from_bytes(config_data[7])
        self.tolerance_to_middle = int.from_bytes(config_data[8])

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)