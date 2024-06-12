# Tracks colour and colour operations
from numpy import average

from logger import logger


# Class to represent RGB colour
class Colour:
    def __init__(self, R: int, G: int, B: int, frequency: int = 1, use_HSV: bool = False) -> None:

        # Grabs the channels
        self.R = R
        self.G = G
        self.B = B

        self.frequency = frequency

        self.use_HSV = use_HSV
        
        # # Enforces each channel to be an int and within an appropriate range
        self.R = max(0, min(255, int(self.R)))
        self.G = max(0, min(255, int(self.G)))
        self.B = max(0, min(255, int(self.B)))
        self.frequency = int(self.frequency)

        # Packages the three channels together
        self.RGB = (self.R, self.G, self.B)

        self.HSV = None

        # Gets HSV for self
        if use_HSV:
            self.get_HSV()

    # Calling the colour returns its RGB or HSV
    def __call__(self) -> tuple[float]:
        if self.use_HSV:
            return self.HSV
        return self.RGB
    
    # tostring
    def __str__(self):
        if self.use_HSV:
            return f'({self.HSV}, {self.frequency})'
        return f'({self.RGB}, {self.frequency})'
    
    # Addition
    def __add__(self, other):
        if isinstance(other, Colour):
            return Colour(
                self.R + other.R,
                self.G + other.G,
                self.B + other.B,
                frequency = (self.frequency + other.frequency) / 2
            )
        elif isinstance(other, int | float):
            return Colour(
                self.R + other,
                self.G + other,
                self.B + other,
                frequency = self.frequency
            )
        elif isinstance(other[1], tuple):
            return self + Colour(other)
        else:
            raise TypeError(f'Colour addition not supported with type "{type(other)}"')
        
    # Subtraction
    def __sub__(self, other):
        if isinstance(other, Colour):
            return Colour(
                self.R - other.R,
                self.G - other.G,
                self.B - other.B,
                frequency = (self.frequency + other.frequency) / 2
            )
        elif isinstance(other, int | float):
            return Colour(
                self.R - other,
                self.G - other,
                self.B - other,
                frequency = self.frequency
            )
        elif isinstance(other[1], tuple):
            return self - Colour(other)
        else:
            raise TypeError(f'Colour subtraction not supported with type "{type(other)}"')
        
    # Multiplication
    def __mul__(self, other):
        return Colour(
            self.R * other,
            self.G * other,
            self.B * other,
            frequency = self.frequency
        )
    
    # Division
    def __truediv__(self, other):
        return Colour(
            self.R / other,
            self.G / other,
            self.B / other,
            frequency = self.frequency
        )
    
    # Gets HSV values
    def get_HSV(self) -> tuple[int]:

        if self.HSV:
            return self.HSV

        # Maps RGP to the range [0,1]
        r = self.R / 255
        g = self.G / 255
        b = self.B / 255

        # Initialises values
        h, s, v = None, None, None

        # Used in calculations
        cmax = max(r, g, b)
        cmin = min(r, g, b)
        diff = cmax - cmin


        # Finds hue
        if cmax == cmin:
            h = 0
        elif cmax == r:
            h = (60 * ((g - b) / diff) + 360) % 360
        elif (cmax == g):
            h = (60 * ((b - r) / diff) + 120) % 360
        elif (cmax == b):
            h = (60 * ((r - g) / diff) + 240) % 360
        
        # Finds saturation
        if cmax == 0:
            s = 0
        else:
            s = diff / cmax * 100

        # Finds value
        v = cmax * 100

        # Gets values
        self.H = int(round(h, 0))
        self.S = int(round(s, 0))
        self.V = int(round(v, 0))
        self.HSV = (self.H, self.S, self.V)
        return self.HSV



# Returns the average colour in a set of colours
def average_colour(colours: list[Colour], weights: list[int] | None = None) -> Colour:
    return Colour(
        average([colour.R for colour in colours], weights = weights),
        average([colour.G for colour in colours], weights = weights),
        average([colour.B for colour in colours], weights = weights),
        frequency = average([colour.frequency for colour in colours]) if not weights else average(weights)
    )

# Same as average_colour(), but where the weights are the frequencies
def weighted_colour(colours: list[Colour], weights: list[int] | None = None) -> Colour:
    if not weights:
        weights = [colour.frequency for colour in colours]
    return average_colour(colours, weights)

# Returns the most common colour in a set
def common_colour(colours: list[Colour]) -> Colour:
    return max(colours, key = lambda x : x.frequency)



# An easy way of getting the list of functions in this file
colour_functions    = [average_colour, weighted_colour, common_colour]
colour_names        = ['Average', 'Weighted', 'Common']