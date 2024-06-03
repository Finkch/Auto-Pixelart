# Tracks colour and colour operations
from numpy import average

# Returns the average colour in a set of colours
def average_colour(colours):

    # In the case `colours` contains frequency information
    if isinstance(colours[0][1], tuple):
        return (
            int(average([colour[0] for colour in colours])),
            get_average_colour(colours)
        )
    
    # When `colours` is only RGB
    else:
        return get_average_colour(colours)

# Same as average_colour(), but where the weights are the occurances
def weighted_colour(colours, weights = None):
    if not weights:
        weights = [colour[0] for colour in colours]

        return (
            int(average(weights)),
            get_average_colour(colours, weights)
        )
    else:
        return get_average_colour(colours, weights)

# Returns the most common colour in a set
def common_colour(colours):
    return max(colours, key = lambda x : x[0])

# Gets the average colour
def get_average_colour(colours, weights = None):

    # One recursive call to remove frequency component
    if isinstance(colours[0][1], tuple):
        return get_average_colour([colour[1] for colour in colours], weights)

    # Averages each channel
    return (
        int(average([colour[0] for colour in colours], weights = weights)),
        int(average([colour[1] for colour in colours], weights = weights)),
        int(average([colour[2] for colour in colours], weights = weights))
    )



# Class to represent RGB colour
class Colour:
    def __init__(self, colour: tuple = None) -> None:

        # In case the colour encodes frequency as well
        if isinstance(colour[1], tuple):
            self.frequency = colour[0]
            self.R = colour[1][0]
            self.G = colour[1][1]
            self.B = colour[1][2]

        # If the colour is only RGB
        else:
            # Sets the channels
            self.R = colour[0]
            self.G = colour[1]
            self.B = colour[2]
        
        # Enforces each channel to be an int and within an appropriate range
        self.R = max(0, min(255, int(self.R)))
        self.G = max(0, min(255, int(self.G)))
        self.B = max(0, min(255, int(self.B)))

        # Packages the three channels together
        self.RGB = [self.R, self.G, self.B]

    # Addition
    def __add__(self, other):
        if isinstance(other, Colour):
            return Colour(
                self.R + other.R,
                self.G + other.G,
                self.B + other.B
            )
        elif isinstance(other, int | float):
            return Colour(
                self.R + other,
                self.G + other,
                self.B + other
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
                self.B - other.B
            )
        elif isinstance(other, int | float):
            return Colour(
                self.R - other,
                self.G - other,
                self.B - other
            )
        elif isinstance(other[1], tuple):
            return self - Colour(other)
        else:
            raise TypeError(f'Colour addition not supported with type "{type(other)}"')
        
    # Multiplication
    def __mul__(self, other):
        return Colour(
            self.R * other,
            self.G * other,
            self.B * other
        )
    
    # Division
    def __truediv__(self, other):
        return Colour(
            self.R / other,
            self.G / other,
            self.B / other
        )




# An easy way of getting the list of functions in this file
colour_functions    = [average_colour, weighted_colour, common_colour]
colour_names        = ['Average', 'Weighted', 'Common']