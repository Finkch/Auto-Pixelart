# For making little images to I can have a better idea at what's going on

from image import Image
from PIL import Image as Pim

from math import log

from logger import logger
from colour import *


# Given an image, visualises its palette
def show_palette(image: Image, use_average = False):

    # Gets the colours
    colours = sorted(image.get_colours(), reverse = True, key = lambda x : x[0])

    # Trims colours down to top 10% or 10, whichever is greater
    # But won't trim if the lengths is already 10 or less
    trimmed = colours[ : min( 
                            max(int(len(colours) / 10), 10)
                        , len(colours) )]


    # Sorts by occurances
    by_occur = sorted(trimmed, reverse = True, key = lambda x : x[0])
    maxi = by_occur[0][0] # Gets the greatest number of occurances - used later

    # Sorts by colour
    by_colour = sorted(trimmed, reverse = True, key = lambda x : (x[1][0], x[1][1], x[1][2]))

    # Sorts by lightness
    by_light = sorted(trimmed, reverse = True, key = lambda x : x[1][0] + x[1][1] + x[1][2])

    # Bundles the three choices
    palettes = [by_occur, by_colour, by_light]


    # Logs the colour list
    logger.log('colour_listing',
        [f'{str(colour)}\t{colour[0] / (image.source.width * image.source.width)}%\n' for colour in by_occur],
        [f'{str(colour)}\t{colour[0] / (image.source.width * image.source.width)}%\n' for colour in by_colour],
        [f'{str(colour)}\t{colour[0] / (image.source.width * image.source.width)}%\n' for colour in by_light],
        [f'{str(colour)}\t{colour[0] / (image.source.width * image.source.width)}%\n' for colour in colours],
        )
    

    # Gets the width of the palette image
    # Set a cap on the width
    max_width = 2000
    width = min(len(by_occur), max_width)
    im_width = max(int(width * 1.1), width + 2) # Accounts for very small palettes

    # Gets the height of the image
    height = 500 # The height as seen by a row
    row_height = int(height * 1.05)
    im_height = int(len(palettes) * row_height)

    # colours per pixel
    # Used for when the image is too small to show all colours
    cpp = 1
    if len(by_occur) > width:
        cpp = len(by_occur) / width


    # Creates a white image, which will be editted to show the palette
    nim = Pim.new(mode = 'RGB', size = (im_width, im_height), color = 'white')

    # Obtains the map to pixels in the new image
    pixels = nim.load()


    # Paints the three palette visualisations onto the image
    for k in range(len(palettes)):

        # Calculates some constants per palette
        x_off = int((im_width - width) / 2)
        y_off = int((row_height - height) / 2 + k * row_height)

        # Iterates over each colour
        for i in range(width):

            # Chooses the colour to represent by which is the most occuring
            colour = palettes[k][i]
            if cpp > 1:

                # Obtains the set of colours to represent in this column
                sub = palettes[k][int(i * cpp) : int(cpp * (i + 1))]

                # Chooses the most common colour
                if use_average:
                    colour = average_colour(sub)
                else:
                    colour = common_colour(sub)


            # Maps the height to be in a reasonable range
            mapped = int((log(colour[0], maxi) / 2 + 0.5) ** 5 * height)

            # Gets the position in the row; centred vertically
            start = int((height - mapped) / 2)
            stop = height - start

            # Paints the coloumn
            for j in range(start, stop):
                pixels[i + x_off, j + y_off] = colour[1]


    # Saves the image
    nim.save(f'outputs/palette_{image.file}')