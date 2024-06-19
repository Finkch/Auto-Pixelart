# For making little images to I can have a better idea at what's going on

from image import Image
from palette import Palette
import matplotlib.pyplot as plt
import numpy as np
import PIL.Image as Pim

from math import log, sin, cos, pi

from numpy import array
from colorsys import hsv_to_rgb


# Paints a colour wheel to visualise an image's palette
def show_colour_wheel(image: Image, palette: Palette) -> None:
    
    # Converts the image to HSV
    image = image.convert('HSV')

    # Gets the palette associated with the colours
    colours = image.palette()

    # Saves just the palette
    palette.paint(150).convert('RGB').save(f'outputs/palettestrip_{image.file_name}.png')

    # Dimensions of the visualisation
    d = 256
    bw = 4
    bh = 4
    r = 4

    source = Pim.new('HSV', size = (2 * d + bw, d + bh), color='blue')

    # Access to the pixel
    pixel_map = source.load()


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
    for colour in colours.colours:
        h = colour[0]
        s = colour[1]
        v = colour[2]

        pixel_map[h, s] = (h, s, 255)
        pixel_map[d + bh + h, v] = (h, 255, v)

    # Paints the palette
    for colour in palette:
        h = colour[0]
        s = colour[1]
        v = colour[2]

        ss = int(s + 255 / 3) % 255
        vv = int(v + 255 / 3) % 255


        # Paints a circle to emphasis the colour
        for k in range(r):
            for rads in range(int(r ** 2)):
                i = int(k * cos(rads / (r ** 2) * 2 * pi))
                j =  int(k * sin(rads / (r ** 2) * 2 * pi))
                try:
                    pixel_map[h + i, s + j] = (h, ss, 255)
                    pixel_map[d + bh + h + i, v + j] = (h, 255, vv)
                except Exception:
                    pass # In case this draws out-of-bounds

    source = source.convert('RGB')
    source.save(f'outputs/palette_{image.file_name}.png')

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
