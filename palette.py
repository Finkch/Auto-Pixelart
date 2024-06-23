# A class to represent an image's palette

from __future__ import annotations

from colour import *

import PIL.Image as Pim

SIMILAR     = 's'
KMEANS      = 'k'
DISSIMILAR  = 'd'
EXTREMAL    = 'e'
SIMDIS      = 'sd'


class Palette(ColourList):
    def __init__(self, image_colours: list, mode: str = 'RGB') -> None:
        super().__init__(image_colours, mode)
    
    # Not that indexing a ColourList gives a frequency-colour pair,
    # indexing a Palette only yields colour.
    def __getitem__(self, index: int) -> tuple:
        return tuple(self.colours[index])

    # Adds item to the palette, albeit inefficiently
    def add(self, colour: tuple) -> Palette:
        return Palette(super().add(colour).data, self.mode)
    
    # Overloads super class's convert, albeit inefficiently
    def convert(self, mode: str) -> Palette:
        return Palette(super().convert(mode).data, mode)
    
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

    # Reduction methods.
    # Valid modes are:
    #   'k':    k-means clustering
    #   's':    combine similar
    #   'd':    build by dissimilar
    #   'e':    n-extremal method
    def reduce(self, size: int = 8, mode: str = 's', *args) -> Palette:
        match mode:
            case 'k':   return self.reduce_kmeans(size)
            case 's':   return self.reduce_similar(size)
            case 'd':   return self.reduce_dissimilar(size)
            case 'e':   return self.reduce_extremal(size, *args)
            case 'sd':  return self.reduce_similar_dissimilar(size, *args)
            case _:     raise ValueError(f'No such palette mode as "{mode}"')

    # Uses k-means clustering to build the palette.
    # Uses PIL's quantisation to do it quickly.
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
        return Palette(image.getcolors(image.width * image.height), self.mode)
    
    # Takes the top n colours (256 by default) found by k-means and
    # reduces it down by combining the most similar colours.
    def reduce_similar(self, size: int) -> Palette:
        
        # Speeds up the process but first reducing to a smaller
        # palette that still is representative
        palette = self.reduce_kmeans(256)

        # Gets a copy of the colours, sorted by ascending frequency.
        # Although the order does not matter much.
        data = sorted(palette.data, key = lambda c: c[0])

        # Gets the function used to find the difference between colours
        colour_difference = colour_difference_HSV if self.mode == 'HSV' else colour_difference_RGB

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

        return Palette(data, mode = self.mode)
    
    # Starts with the most dominent colour, then iteratively
    # adds the most didsimilar colour.
    def reduce_dissimilar(self, size: int) -> Palette:
        
        # Speeds up the process but first reducing to a smaller
        # palette that still is representative
        # NOTE: this is just a list!
        colours = sorted(self.reduce_kmeans(256).data, key = lambda c: c[0])
        
        # Creates the base palette with the most dominent colour.
        # Since the list is sorted, the most dominent item is last.
        palette = [colours.pop()]

        # Converts the palette to a Palette
        palette = Palette(palette, self.mode)

        
        # Iterativey adds the most disimilar colour
        while len(palette) < size:

            # Sorts by disimilarity to the current palette
            colours = sorted(
                colours,
                key = lambda c: palette.similarity(c[1])
            )

            # Adds the least similar colour to the palette
            palette = palette.add(colours.pop())
        
        return palette
    
    # Combines kmeans and dissimilar strategies.
    # Creates a kmeans palette of size `size - extremals`, then
    # populates the rest of the palette with dissimilar values.
    # If `extremals` is None, then `extremals = int(size / 4)`.
    #
    # NOTE: this method approached kmeans if `extremals = 0` and it
    # becomes dissimilar if `extremals = size - 1`.
    def reduce_extremal(self, size: int, extremals: int = None) -> Palette:
        
        # Sets default values
        if extremals == None:
            extremals = min(int(size / 4), 1)

        # Gets a reduced colour set
        colours = sorted(self.reduce_kmeans(256).data, reverse = True, key = lambda c: c[0])

        # Gets the starting palette, removing the colours from the list
        palette = colours[:size - extremals]
        colours = colours[size - extremals:]

        # Converts the palette to a Palette
        palette = Palette(palette, self.mode)

        # Iterativey adds the most disimilar colour
        while len(palette) < size:

            # Sorts by disimilarity to the current palette
            colours = sorted(
                colours,
                key = lambda c: palette.similarity(c[1])
            )

            # Adds the least similar colour to the palette
            palette = palette.add(colours.pop())
        
        return palette
    
    # Reduces the palette down to `size - dissimilars` colours, then
    # goes through again and adds `dissimilars` amount of the most
    # dissimilar colours.
    def reduce_similar_dissimilar(self, size: int, dissimilars: int = None) -> Palette:
        
        # Gets default
        if not dissimilars:
            dissimilars = min(int(size / 4), 1)

        # Gets the palette of similar colours
        palette = self.reduce_similar(size - dissimilars)

        # Gets a reduced colour set
        colours = sorted(self.reduce_kmeans(256).data, reverse = True, key = lambda c: c[0])

        # Iterativey adds the most disimilar colour
        while len(palette) < size:

            # Sorts by disimilarity to the current palette
            colours = sorted(
                colours,
                key = lambda c: palette.similarity(c[1])
            )

            # Adds the least similar colour to the palette
            palette = palette.add(colours.pop())
        
        return palette