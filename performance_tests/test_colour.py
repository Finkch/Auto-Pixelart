# Tested performance of colour

from colour import Colour
from image import Image
from random import randint

# Tests how much performance loss is in calculating both RGB and HSV
''' RESULTS
        It is roughly 2/5ths faster to ignore the HSV values
'''
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
''' RESULTS
        It is roughly 2/5ths faster to ignore the HSV values
'''
def test_image_RGB_HSV(trials):
    args = []

    return args, [image_RGB, image_HSV], ['RGB', 'HSV'], False

# Tests the effectiveness of downsizing an image before getting its palette
''' RESULTS
        Downscaling a bit helps a lot, but downscaling lots doesn't help much.
        1/2 size was 2x as fast, but 1/30 was only 4x as fast.
        > 0.927s for Nora.jpg at original size (3072px)
        > 0.483s for Nora.jpg at ~half size (1500px)
        > 0.241s for Nora.jpg at ~1/30th size (100px)
'''
def test_get_palette(trials):
    args = []

    return args, [image_palette_raw, image_palette_downscale_1500, image_palette_downscale_100], ['No downscale (3072)', '1500', '100'], False

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

# Downscaling or not for getting image palette
def image_palette_raw() -> Image:
    image = Image(HSV = False)
    image.set_file('Nora.jpg')
    image.get_palette(16)
    return image

def image_palette_downscale_1500() -> Image:
    image = Image(HSV = False)
    image.set_file('Nora.jpg')
    image.get_palette(16, width = 1500)
    return image

def image_palette_downscale_100() -> Image:
    image = Image(HSV = False)
    image.set_file('Nora.jpg')
    image.get_palette(16, width = 100)
    return image