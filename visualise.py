# For making little images to I can have a better idea at what's going on

from image import Image
from palette import Palette
import matplotlib.pyplot as plt
import numpy as np
import PIL.Image as Pim

from math import sin, cos, pi

from numpy import array
from colorsys import hsv_to_rgb

# Paints a colour wheel to visualise an image's palette
def show_colour_wheel(image: Image, palette: Palette) -> None:
    
    # Gets a copy of the RGB palette because we need RGB
    # colours to paint in matplotlib
    palette_rgb = palette.convert('RGB')

    # Ensures palette and image are HSV
    image = image.convert('HSV')
    palette = palette.convert('HSV')

    # Save the palette
    palette_rgb.paint(150).save(f'outputs/palettestrip_{image.file_name}.png')


    # Gets the colours in the image.
    # Use a palette object for easier indexing
    colours = image.palette()


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
def show_3d(image: Image, palette: Palette) -> None:

    # Converts the image and palette to HSV
    image = image.convert('HSV')
    palette = palette.convert('HSV')

    # Grabs components of the colourlist
    colours = image.colours()
    data = colours.data[::5]                    # Step of 5 for performance
    frequencies = data[:, 0].astype('float')    # To prevent np.log int-type issues
    colours = colours.colours[::5]

    # Converts the colours to an appropriate range of 0-1 (and to RGB)
    colours_RGB = array([hsv_to_rgb(*(colour / 255)) for colour in colours])
    

    # Finds the most occuring colour for normalisation
    maxi = max(data, key = lambda x: x[0])

    # Gets the marker size.
    # Uses very similar mapping to show_colour().
    alphas = ((np.log(frequencies) / np.log(maxi[0])) / 2 + 0.5) ** 5
    sizes = 2


    # Maps the colours to an appropriate range and shifts the palette
    # marker colours away form the cooridnate colours to improve visibility
    palette_RGB = array([hsv_to_rgb(*(colour / 255)) for colour in palette.colours])
    
    # Adds an offset to the hue
    palette_RGB[:, 0] += 1 / 3
    palette_RGB[:, 0] %= 1

    # Size of each point
    psize = 100
    

    # Create the 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot each point with the corresponding color
    ax.scatter(
        colours[:, 0], 
        colours[:, 1], 
        colours[:, 2], 
        c = colours_RGB, marker = 'o', s = sizes, alpha = alphas
    )
    ax.scatter(
        palette.colours[:, 0], 
        palette.colours[:, 1], 
        palette.colours[:, 2], 
        c = palette_RGB, marker = 'X', s = psize
    )

    # Set labels
    ax.set_xlabel('Hue')
    ax.set_ylabel('Saturation')
    ax.set_zlabel('Value')

    plt.show()
