# A class to represent an image's palette

from __future__ import annotations

from numpy import array, ndarray
from colour import *

import PIL.Image as Pim

from logger import logger


class Palette(ColourList):
    def __init__(self, image_colours: list, mode: str = 'RGB') -> None:
        super().__init__(image_colours, mode)
    
    # Not that indexing a ColourList gives a frequency-colour pair,
    # indexing a Palette only yields colour.
    def __getitem__(self, index: int) -> tuple:
        return tuple(self.colours[index])
    
    # Paints the palette into a PIL.Image.
    # This paints unfairly, painting one pixel of each
    # colour before repeating, painting a colour no more
    # times than its frequency.
    def paint_unfair(self, downscale_factor: int = 1):
        length = int((sum(self.frequencies) / downscale_factor) ** 0.5)
        area = int(length ** 2) # This order is to prevent rounding errors

        # Sorts colours by decreasing occurances
        data = sorted(self.data, reverse = True, key = lambda c: c[0])

        # Creates new PIL image
        image = Pim.new(self.mode, (length, length))
        pixels = image.load()

        # Paints new image
        f = 0   # Frequency cutoff
        i = 0   # Iteration
        while i < area:

            # Recomputes len of data for slight increase in efficiency
            datas = len(data)
            for j in range(datas):

                # Since i is incremented in this loop, we need to check
                # the break condition here as well.
                if i >= area:
                    break

                # Finds x, y coordiantes on the image
                x, y = i % length, int(i / length)

                # Paints the pixel the appropriate colour
                pixels[x, y] = tuple(data[j][1])

                # Trims off colours that are too infrequent
                if j == datas - 1:
                    f += 1

                    # Finds colours that are below frequency cutoff
                    s = None
                    for k in range(datas):
                        if data[k][0] == f:
                            s = k
                            break

                    # Trims data. Since data is sorted, we only neeed
                    # the index of the first item below the cutoff
                    if s:
                        data = data[:s]
                i += 1

        return image
    
    # Paints the palette as a palette.
    # One tall, one pixel per colour.
    def paint(self, upscale_factor: int = 1) -> Pim.Image:
        
        # Creates a new image
        image = Pim.new(self.mode, (len(self), 1))
        pixels = image.load()

        # Paints the image with the palette
        for i in range(len(self)):
            pixels[i, 0] = self[i]

        # Upscales the image
        if upscale_factor > 1:
            image = image.resize(
                (image.width * upscale_factor, image.height * upscale_factor), 
                resample = Pim.NEAREST
            )
        
        return image


    # Reduction methods
    def reduce_kmeans(self, size: int) -> Palette:
        
        # Paints an image of the palette so PIL's native
        # k-mean clustering can be used.
        image = self.paint_unfair()

        # Can't quantise HSV images
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Uses PIL for k-means clustering
        image = image.quantize(size)

        # Puts the image back into the correct mode
        if image.mode != self.mode:
            image = image.convert(self.mode)

        # Builds new Palette
        return Palette(image.getcolors(image.width * image.height), image.mode)
    
    def reduce_similar(self, size: int) -> Palette:
        
        # Speeds up the process but first reducing to a smaller
        # palette that still is representative
        palette = self.reduce_kmeans(256)

        # Gets a copy of the colours, sorted by ascending frequency.
        # Although the order does not matter much.
        data = sorted(palette.data, key = lambda c: c[0])

        # Gets the function used to find the difference between colours
        colour_difference = colour_difference_HSV if palette.mode == 'HSV' else colour_difference_RGB

        # Iteratively reduces the palette
        while len(data) > size:

            # Finds the most similar pair
            x, y = -1, -1
            mini = 1e9 # A really big number
            for i in range(len(data) - 1):
                for j in range(i + 1, len(data)):

                    diff = colour_difference(data[i], data[j])

                    # If this pair of colours is more similar
                    # than the last pair, update
                    if diff < mini:
                        mini = diff
                        x, y = i, j

            # Averages the colour and adds it back to the palette.
            # Notice y is popped first sice y > x.
            data.append(average_colour(
                    ColourList([data.pop(y), data.pop(x)], self.mode)
            ))

        return Palette(ColourList(data, mode = self.mode))
