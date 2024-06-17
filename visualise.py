# For making little images to I can have a better idea at what's going on

from image import Image
import matplotlib.pyplot as plt
import numpy as np

from math import log, sin, cos, pi

from colour import *
from numpy import array
from colorsys import hsv_to_rgb

from logger import logger


# Given an image, visualises its colours
def show_colours(image: Image, choose = weighted_colour, choose_name = 'weighted', use_HSV = False):

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
    palette = Image(
        f'colours_{image.file_name} ({choose_name}, {col_type}).{image.file_extension}', 
        location = 'outputs', 
        size =(im_width, im_height)
    )

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
    return palette

# Paints a colour wheel to visualise an image's palette
def show_colour_wheel(image: Image):
    
    # Grabs the colours
    colours = image.get_colours(use_HSV = True)

    # Gets the palette associated with the colours
    palette = image.get_palette(use_HSV = True).palette

    # Saves just the palette
    image.palette.save(image.file_name)


    # Dimensions of the visualisation
    d = 256
    bw = 4
    bh = 4
    r = 4

    # Output image
    output = Image(
        f'wheel_{image.file}',
        location = 'outputs',
        size = (2 * d + bw, d + bh),
        HSV = True
    )

    # Access to the pixel
    pixel_map = output.source.load()


    # Paints a line to separate the two
    for i in range(bw):
        for j in range(d + bh):
            pixel_map[d + i, j] = (0, 0, 0)

    # Paints a small rainbow at the bottom for comparison
    for i in range(d):
        for j in range(bh):
            pixel_map[i, d + j] = (i, 255, 255)
            pixel_map[d + bw +  i, d + j] = (i, 255, 255)


    # Paints the colours
    for colour in colours:
        h = colour.H
        s = colour.S
        v = colour.V

        pixel_map[h, s] = (h, s, 255)
        pixel_map[d + bh + h, v] = (h, 255, v)

    # Paints the palette
    for colour in palette:
        h = colour.H
        s = colour.S
        v = colour.V

        ss = int(s + 255 / 3) % 255
        vv = int(v + 255 / 3) % 255


        # Paints a circle
        for k in range(r):
            for rads in range(int(r ** 2)):
                i = int(k * cos(rads / (r ** 2) * 2 * pi))
                j =  int(k * sin(rads / (r ** 2) * 2 * pi))
                try:
                    pixel_map[h + i, s + j] = (h, ss, 255)
                    pixel_map[d + bh + h + i, v + j] = (h, 255, vv)
                except Exception:
                    pass # In case this draws out-of-bounds

    # Upsizes the output
    output.resize(scale = 0.5, absolute = False)

    return output

# Uses HSV to plot in 3D
def show_3d(image: Image, HSV: bool = True) -> Image:
    
    # This is a plot, not an image. No need to save
    output = Image(None)

    # Separetes the colour and frequency components
    image_colours = image.get_colours(use_HSV = HSV)[::5]
    colours = array([colour() for colour in image_colours])
    frequencies = array([colour.frequency for colour in image_colours]) 

    # Separates the colour into its components
    h = colours[:, 0]
    s = colours[:, 1]
    v = colours[:, 2]

    # Converts the colours to an appropriate range of 0-1 (and to RGB)
    if HSV:
        colours_RGB = array([hsv_to_rgb(*(colour / 255)) for colour in colours])
    else:
        colours_RGB = colours / 255
    

    # Finds the most occuring colour for normalisation
    maxi = max(image_colours, key = lambda x: x.frequency)

    # Gets the marker size.
    # Uses very similar mapping to show_colour().
    alphas = ((np.log(frequencies) / np.log(maxi.frequency)) / 2 + 0.5) ** 5
    sizes = 2

    # sizes = (2 * ((np.log(frequencies) / np.log(maxi.frequency)) / 2 + 0.5)) ** 5
    # alphas = 0.02



    # Gets the palette associated with the colours
    palette = image.get_palette(use_HSV = HSV).palette
    palette_colours = array([colour() for colour in palette])

    # Separates the colour into its components
    ph = palette_colours[:, 0]
    ps = palette_colours[:, 1]
    pv = palette_colours[:, 2]

    if HSV:
        palette_RGB = array([hsv_to_rgb(*(colour / 255)) for colour in palette_colours])
        
        # Adds an offset to the hue
        palette_RGB[:, 0] += 1 / 3
        palette_RGB[:, 0] %= 1
    else:
        palette_RGB = palette_colours / 255

        # Swaps order of colours for better visibility (most of the time)
        palette_RGB[:, 0], palette_RGB[:, 1], palette_RGB[:, 2] = palette_RGB[:, 1], palette_RGB[:, 2], palette_RGB[:, 0]

    # Size of each point
    psize = 100

    

    # Create the 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot each point with the corresponding color
    ax.scatter(h, s, v, c = colours_RGB, marker = 'o', s = sizes, alpha = alphas)
    ax.scatter(ph, ps, pv, c = palette_RGB, marker = 'X', s = psize)

    # Set labels
    if HSV:
        ax.set_xlabel('Hue')
        ax.set_ylabel('Saturation')
        ax.set_zlabel('Value')
    else:
        ax.set_xlabel('R')
        ax.set_ylabel('G')
        ax.set_zlabel('B')

    plt.show()

    return output



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