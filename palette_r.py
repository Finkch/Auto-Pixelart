# A class to represent an image's palette

from __future__ import annotations

from numpy import array, ndarray
from colour_r import ColourList

import PIL.Image as Pim

from logger import logger


class Palette:
    def __init__(self, colours: ColourList) -> None:
        self.palette    = colours

    # Calling a Palette returns its colours
    def __call__(self) -> ndarray:
        return self.palette()
    
    # Other magic methods
    def __len__(self) -> int:
        return len(self.palette)
    
    # Paints the palette into a PIL.Image.
    # This paints unfairly, painting one pixel of each
    # colour before repeating, painting a colour no more
    # times than its frequency.
    def paint_unfair(self, downscale_factor: int = 1):
        length = int((sum(self.palette.frequencies) / downscale_factor) ** 0.5)
        area = int(length ** 2) # This order is to prevent rounding errors

        # Sorts colours by decreasing occurances
        data = sorted(self.palette.data, reverse = True, key = lambda c: c[0])

        # Creates new PIL image
        image = Pim.new(self.palette.mode, (length, length))
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
                pixels[x, y] = data[j][1]

                # Trims off colours that are too infrequent
                if j == datas - 1:
                    f += 1

                    # Finds colours that are below frequency cutoff
                    s = None
                    for k in range(datas):
                        if data[k][1] == f:
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
        image = Pim.new(self.palette.mode, (len(self), 1))
        pixels = image.load()

        # Paints the image with the palette
        for i in range(len(self)):
            pixels[i, 0] = self.palette.colours[i]

        # Upscales the image
        if upscale_factor > 1:
            image = image.resize(
                (image.width * upscale_factor, image.height * upscale_factor), 
                resample = Pim.NEAREST
            )
        
        return image


    # Reduction methods
    def reduce_kmeans(self, size: int) -> Palette:
        
        # Paints an image
        image = self.paint_unfair()

        # Can't quantise HSV images
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Uses PIL for k-means clustering
        image = image.quantize(size)

        # Puts the image back into the correct mode
        if image.mode != self.palette.mode:
            image = image.convert(self.palette.mode)

        # Builds new Palette
        return Palette(ColourList(image.getcolors(image.width * image.height), image.mode))