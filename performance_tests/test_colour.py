# Tested performance of colour

from colour import Colour
from random import randint

# Tests how much performance loss is in calculating both RGB and HSV
def test_RGV_HSV(trials):

    # Each trial will use a random colour
    args = [
        [randint(0, 255),
         randint(0, 255),
         randint(0, 255)]
            for i in range(trials)
    ]

    return args, [colour_RGB, colour_HSV], ['RGB', 'HSV'], True

# Creates an RGB colour
def colour_RGB(r: int, g: int, b: int) -> Colour:
    return Colour(r, g, b, use_HSV = False)

# Creates an HSV colour
def colour_HSV(r: int, g: int, b: int) -> Colour:
    return Colour(r, g, b, use_HSV = True)