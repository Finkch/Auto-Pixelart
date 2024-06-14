from colour import Colour, closest_colour
from image import Image
from PIL.Image import LANCZOS, NEAREST
import PIL.Image as Pim

# Current implementation:
#   1: Downscale image (sinc) to desired size
#   2: For each pixel, find which in the palette is the closet
#   3: Repaint as closest colour
def palettised(input: Image, output: Image) -> Image:
    
    return put_palette(input, output)


def pil_palette(input: Image, output: Image) -> Image:

    # Creates a copy of the image
    output.source = input.source.copy()

    # Creates and sets a colour palette
    output.source = output.source.convert(
        'P', 
        palette = Pim.ADAPTIVE,
        colors = output.palette_size
    )

    # Downscales to desired size
    output.source.thumbnail((output.width, output.height))

    # Returns
    return output

def put_palette(input: Image, output: Image) -> Image:
    
    # Obtains the palette
    palette = input.get_palette(output.palette_size)

    # Converts the palette into PIL palette
    pilette = []
    for colour in palette:
        pilette.append(colour.R)
        pilette.append(colour.G)
        pilette.append(colour.B)

    # Creates an image of the palette
    palette_image = Pim.new('P', (output.palette_size, 1))
    palette_image.putpalette(pilette)

    # Quantises the image to use the palette image's colours
    output.source = input.source.quantize(palette = palette_image, dither = 0)

    # Downsizes
    output.source.thumbnail((output.width, output.height), resample = NEAREST)

    return output


def paint_palette(input: Image, output: Image) -> Image:
    
    # Gets the palette of the image
    palette = input.get_palette(output.palette_size)

    # Downscales the original image
    output.source = input.source.resize((output.width, output.height), resample = NEAREST)

    # Pixel map of the source and downscaled
    pixel_map = output.source.load()

    # A map of colouring to speed up the process
    palette_map = {}

    # Iterates over every pixel to paint
    for i in range(output.width):
        for j in range(output.height):

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

    return output