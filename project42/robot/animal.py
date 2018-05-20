"""Animal module"""

class Animal:
    """Represents an animal."""
    def __init__(self, config_data):
        self.lower_color = (config_data[0], config_data[1], config_data[2])
        self.upper_color = (config_data[3], config_data[4], config_data[5])
        self.min_contour_size = config_data[6]
        self.contour_type = config_data[7]
        self.tolerance_to_middle = config_data[8]