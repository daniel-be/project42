"""Animal module"""

class Animal:
    """Represents an animal."""
    def __init__(self, lower_color, upper_color, min_contour_size, contour_type, tolerance_to_middle):
        self.lower_color = lower_color
        self.upper_color = upper_color
        self.min_contour_size = min_contour_size
        self.contour_type = contour_type
        self.tolerance_to_middle = tolerance_to_middle

class Animals:
    """Holds the different animals."""
    Frog = Animal((29, 100, 60), (64, 255, 255), 30, "Rectangle", 40)
    Tomato = Animal((0, 50, 50), (10, 255, 255), 20, "Circle", 40)
    Rhino = Animal((56, 59, 0), (164, 255, 72), 20, "Circle", 40)
    Leopard = Animal((0, 77, 26), (23, 255, 157), 6000, "Rectangle", 40)
    Turtle = Animal((7, 16, 103),(23, 98, 138), 20, "Circle", 60)