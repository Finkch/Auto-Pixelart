# Tracks colour and colour operations
from numpy import average

from logger import logger


# Class to represent RGB colour
class Colour:
    def __init__(self, R: int, G: int, B: int, frequency: int = 1) -> None:

        # Grabs the channels
        self.R = R
        self.G = G
        self.B = B

        self.frequency = frequency
        
        # # Enforces each channel to be an int and within an appropriate range
        self.R = max(0, min(255, int(self.R)))
        self.G = max(0, min(255, int(self.G)))
        self.B = max(0, min(255, int(self.B)))
        self.frequency = int(self.frequency)

        # Packages the three channels together
        self.RGB = (self.R, self.G, self.B)
    
    # tostring
    def __str__(self):
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