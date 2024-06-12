# Tested performance of colour

from colour import Colour
from image import Image
from random import randint

# Tests how much performance loss is in calculating both RGB and HSV
def test_RGB_HSV(trials):

    # Each trial will use a random colour
    args = [
        [randint(0, 255),
         randint(0, 255),
         randint(0, 255)]
            for i in range(trials)
    ]

    return args, [colour_RGB, colour_HSV], ['RGB', 'HSV'], True

# Tests how much performance loss is in calculating both RGB and HSV
def test_image_RGB_HSV(trials):
    args = []

    return args, [image_RGB, image_HSV], ['RGB', 'HSV'], False

# For colour variation of RGB vs HSV test
def colour_RGB(r: int, g: int, b: int) -> Colour:
    return Colour(r, g, b, use_HSV = False)

def colour_HSV(r: int, g: int, b: int) -> Colour:
    return Colour(r, g, b, use_HSV = True)


# For image variation of RGB vs HSV test
def image_RGB() -> Image:
    image = Image(HSV = False)
    image.set_file('Nora.jpg')
    return image

def image_HSV() -> Image:
    image = Image(HSV = True)
    image.set_file('Nora.jpg')
    return image