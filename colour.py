# Tracks colour and colour operations

from image import Image

class Colour:
    def __init__(self, R: int = 0, G: int = 0, B: int = 0):
        self.R = R
        self.G = G
        self.B = B



# Returns a list of 
def count_colours(image: Image) -> dict:

    # Contains colour counts
    #   key:    (R, G, B) as a tuple of integers
    #   value:  integer count
    counts = {}

    # Get data returns an iterable of tuples
    for colour in image.source.getdata():

        # Adds key to the dictionary if it isn't present
        if colour not in counts:
            counts[colour] = 0
        

        # Increments the count of that colour
        counts[colour] += 1

    return counts