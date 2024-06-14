# For making little images to I can have a better idea at what's going on

from image import Image
from PIL import Image as Pim

from math import log

from logger import logger
from colour import *


# Given an image, visualises its palette
def show_palette(image: Image, choose = weighted_colour, choose_name = 'weighted', use_HSV = False):

    # Obtains the set of palettes and the most common element
    palettes, maxi = colourings(image.get_colours(), use_HSV)

    # Appends the sorting method
    col_type = 'RGB'
    if use_HSV:
        col_type = 'HSV'

    # Logs the colour list
    logger.log('colour_listing',
        *[[f'{colour}\t{colour.frequency / (image.width * image.width)}%\n' for colour in palette
                ] for palette in palettes]
    )
    

    # Gets the width of the palette image
    # Set constraints on width
    max_width = 2000
    min_width = 200
    width = max(min(len(palettes[0]), max_width), min_width)
    im_width = max(int(width * 1.1), width + 2) # Accounts for very small palettes

    # Gets the height of the image
    # Since height depends on width, height is also constrained
    height = max(int(width / 3), 100)
    row_height = int(height * 1.05)
    im_height = int(len(palettes) * row_height)

    # Used for when the image is too small to show all colours
    # cpp: colours per pixel
    cpp = len(palettes[0]) / width


    # Creates a white image, which will be editted to show the palette
    palette = Image(f'palette_{image.file_name} ({choose_name}, {col_type}).{image.file_extension}', location = 'outputs', size =(im_width, im_height))

    # Obtains the map to pixels in the new image
    pixels = palette.source.load()


    # Paints the three palette visualisations onto the image
    for k in range(len(palettes)):

        # Calculates some constants per palette
        x_off = int((im_width - width) / 2)
        y_off = int((row_height - height) / 2 + k * row_height)

        # Iterates over each colour
        for i in range(width):

            # Chooses the colour to represent by which is the most occuring
            colour = palettes[k][int(i * cpp)]
            if cpp > 1:

                # Obtains the set of colours to represent in this column
                sub = palettes[k][int(i * cpp) : int(cpp * (i + 1))]

                # Chooses a single colour
                # `choose()` was passed as an argument during the `show_palette()` call!
                colour = choose(sub)


            # Maps the height to be in a reasonable range
            mapped = int((log(colour.frequency, maxi.frequency) / 2 + 0.5) ** 5 * height)

            # Gets the position in the row; centred vertically
            start = int((height - mapped) / 2)
            stop = height - start

            # Paints the coloumn
            for j in range(start, stop):
                pixels[i + x_off, j + y_off] = colour.RGB

    # Saves the image
    palette.save()
    return palette


# Returns a list of possible ways to visualise the palette.
#   NOTE: this also return the most common element, which 
#   is used in calculations later.
def colourings(colours: list[Colour], use_HSV: bool = False) -> tuple[list, Colour]:

    # Sorts colours by frequency    
    colours = sorted(colours, reverse = True, key = lambda x : x.frequency)

    # Trims colours down to top 10% or 10, whichever is greater
    # But won't trim if the lengths is already 10 or less
    trimmed = colours[ : min( 
                            max(int(len(colours) / 10), 10)
                        , len(colours) )]


    if use_HSV:
        return HSV_colourings(trimmed)
    
    return RGB_colourings(trimmed)

def RGB_colourings(colours: list[Colour]) -> tuple[list, Colour]:

    # Sorts by colour
    by_colour = sorted(colours, reverse = True, key = lambda x : list(x.RGB))

    # Sorts by lightness
    by_light = sorted(colours, reverse = True, key = lambda x : sum(x.RGB))

    # Bundles the choices
    return [colours, by_colour, by_light], colours[0]

def HSV_colourings(colours: list[Colour]) -> tuple[list, Colour]:

    # Updates each colour with its HSV
    [colour.get_HSV() for colour in colours]

    # By hue
    by_hue = sorted(colours, reverse = True, key = lambda x: (x.H, x.V))

    # By saturation
    by_saturation = sorted(colours, reverse = False, key = lambda x: (x.S, x.H))

    # By value
    by_value = sorted(colours, reverse = True, key = lambda x: (x.V, x.H))

    # Bundles the choices
    return [colours, by_hue, by_saturation, by_value], colours[0]