"""Animal module"""

class Animal:
    """Represents an animal."""
    def __init__(self, lower_color, upper_color, min_contour_size, contour_type):
        self.lower_color = lower_color
        self.upper_color = upper_color
        self.min_contour_size = min_contour_size
        self.contour_type = contour_type

class Animals:
    """Holds the different animals."""
    Frog = Animal((29, 100, 60), (64, 255, 255), 30, "Rectangle")
    Tomato = Animal((0, 50, 50), (10, 255, 255), 20, "Circle")
    Rhino = Animal((90, 50, 50), (130, 255, 255), 20, "Circle")
    #Leopard = Animal((90, 50, 50), (130, 255, 255), 30, "Rectangle")