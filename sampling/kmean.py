from colour import Colour, closest_colour
from image import Image
from PIL.Image import LANCZOS, NEAREST
import PIL.Image as Pim

# Current implementation:
#   1: Downscale image (sinc) to desired size
#   2: For each pixel, find which in the palette is the closet
#   3: Repaint as closest colour
def palettised(image: Image, pixel_art: Image, log: bool = False) -> Image:
    
    return paint_palette(image, pixel_art, log)


def pil_palette(image: Image, pixel_art: Image, log: bool = False) -> Image:

    # Creates a copy of the image
    pixel_art.source = image.source.copy()

    # Creates and sets a colour palette
    pixel_art.source = pixel_art.source.convert(
        'P', 
        palette = Pim.ADAPTIVE,
        colors = pixel_art.palette_size
    )

    # Downscales to desired size
    pixel_art.source.thumbnail((pixel_art.width, pixel_art.height))

    # Returns
    return pixel_art

def put_palette(image: Image, pixel_art: Image, log: bool = False) -> Image:
    
    # Obtains the palette
    palette = image.get_palette(pixel_art.palette_size)

    # Converts the palette into PIL palette
    pilette = []
    for colour in palette:
        pilette.append(colour.R)
        pilette.append(colour.G)
        pilette.append(colour.B)

    # Creates an image of the palette
    palette_image = Pim.new('P', (pixel_art.palette_size, 1))
    palette_image.putpalette(pilette)

    # Quantises the image to use the palette image's colours
    pixel_art.source = image.source.quantize(palette = palette_image, dither = 0)

    # Downsizes
    pixel_art.source.thumbnail((pixel_art.width, pixel_art.height), resample = NEAREST)

    return pixel_art


def paint_palette(image: Image, pixel_art: Image, log: bool = False) -> Image:
    
    # Gets the palette of the image
    palette = image.get_palette(pixel_art.palette_size)

    # Downscales the original image
    pixel_art.source = image.source.resize((pixel_art.width, pixel_art.height), resample = NEAREST)

    # Pixel map of the source and downscaled
    pixel_map = pixel_art.source.load()

    # A map of colouring to speed up the process
    palette_map = {}

    # Iterates over every pixel to paint
    for i in range(pixel_art.width):
        for j in range(pixel_art.height):

            # Gets the colour
            colour = Colour(*pixel_map[i, j])

            # Gets a tuple of the colour
            ct = tuple(colour.RGB)

            # Adds the colour and its corresponding colour
            # in the palette to the map. This improbes
            # performance for repeat colours.
            if colour not in palette_map:
                palette_map[ct] = tuple(closest_colour(palette, colour).RGB)

            # Paints the corresponding pixel
            pixel_map[i, j] = palette_map[ct]

    return pixel_art