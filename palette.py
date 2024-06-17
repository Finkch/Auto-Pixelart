# Finds and defines palettes

from numpy import array, ndarray
import numpy as np
import PIL.Image as Pim
from PIL.ImageFilter import Kernel
from PIL.Image import NEAREST
from colour import Colour
from math import ceil
from sklearn.cluster import KMeans

from logger import logger

class Palette:
    def __init__(self, source: Pim.Image, colours: int = 8, HSV: bool = False) -> None:
        self.source = source
        self.colours = int(colours)
        self.HSV = HSV
        self.palette = self.get()

    # Calling a Palette will return an ndarray of values
    def __call__(self) -> ndarray[tuple]:
        return array([colour() for colour in self.palette])
    
    # Returns a deep copy of the palette
    def copy(self, use_HSV: bool = None):

        HSV = self.HSV
        if not use_HSV == None:
            HSV = use_HSV

        return Palette(
            self.image(),
            self.colours,
            HSV
        )

    
    # Returns an image representation of the palette
    def image(self, palette: ndarray[Colour] = None) -> Pim.Image:

        if isinstance(palette, type(None)):
            palette = self.palette

        # Gets the dimensions of the image
        width   = min(len(palette), 16)
        height  = int(ceil(len(palette) / 16))

        # Gets the required image mode
        mode = 'HSV' if self.HSV else 'RGB'
        colour = 'blue' if self.HSV else 'white' # RGB blue is white in HSV

        # Creates output image
        output = Pim.new(
            mode    = mode, 
            size    = (width, height), 
            color   = colour
        )

        # Gets access to the pixels
        pixel_map = output.load()

        print(width, height)

        # Colours the image to be the 
        for j in range(height):
            for i in range(width):
                pixel_map[i, j] = palette[i + j * 16]()


        # HSV files cannot be saved, annoyingly
        if self.HSV:
            output = output.convert('RGB')

        return output


    # Saves the palette as an image
    def save(self, file_name: str) -> Pim.Image:

        # Gets the image
        output = self.image()

        # Saves minimum sized image
        output.save(f'palettes/{file_name}.png')

        # Saves a reasonably sized version
        output = output.resize((output.width * 150, output.height * 150), resample = NEAREST)
        output.save(f'palettes/{file_name}_large.png')

        return output

    # Gets best representation for the image's palette.
    def get(self, dwidth: int = None) -> ndarray[Colour]:

        # Gets a copy of the image to process
        image = self.source.copy()

        # Automatically grabs the palette size for palette images
        if self.colours == -1:
            return self.from_palette_image(image)

        # Reduces image size to speed up the computation
        if dwidth:
            dheight = int(dwidth / image.width * image.height)
            image.thumbnail((dwidth, dheight))

        return self.get_extremal1(image)

    # Based on StackOverflow code: https://stackoverflow.com/questions/3241929/how-to-find-the-dominant-most-common-color-in-an-image
    def get_auto(self, image: Pim.Image, colours: int = None) -> ndarray[Colour]:

        if not colours:
            colours = self.colours

        # Reduces the colours in the image.
        # Internally, k-mean clustering is used
        paletted = image.convert('P', palette = Pim.ADAPTIVE, colors = colours)
        image_palette = paletted.getpalette()

        # Retrieves a list of dominent colours
        colour_counts = sorted(paletted.getcolors(), reverse = True)

        # Gets the top dominent colours
        palette = []
        for i in range(len(colour_counts)):

            # Gets the index of the item
            pindex = colour_counts[i][1]

            # Palette is just a list of values (not tuples), 
            # so we need to stride over items
            palette.append(Colour(*image_palette[pindex * 3 : pindex * 3 + 3], use_HSV = self.HSV))

        return array(palette)
    
    # Used with palette images
    def from_palette_image(self, source_copy: Pim.Image) -> ndarray[Colour]:
        
        # Gets the colours in the image
        colours = source_copy.getcolors()

        # Updates colour count
        self.colours = len(colours)

        # Gets Colours in the palette
        palette = [Colour(*colour[1]) for colour in colours]

        return array(palette)

    # Recursively finds the palette
    def get_recursive(self, image: Pim.Image) -> ndarray[Colour]:
        
        starting_size = 256

        # Gets the palette image using large colour count
        self.palette = self.get_auto(image, starting_size)
        palette_image = self.image()


        # Uses recursion to reduce the palette until it's the desired size
        return self.get_recursive_step(palette_image, starting_size)

    def get_recursive_step(self, palette_image: Pim.Image, colours: int) -> ndarray[Colour]:
        
        nim = palette_image.convert('RGB').resize((palette_image.width * 150, palette_image.height * 150) ,resample = NEAREST)
        nim.save(f'temp/palette_{colours}.png')

        # Base case.
        # Returns the palette
        if colours == self.colours:
            return self.get_auto(palette_image)

        # Finds the required number of colours for the next step.
        # Halves the number of colours from this step, unless it
        # would cause a miss of the base case.
        next_colours = int(colours / 2)
        if next_colours < self.colours:
            next_colours = self.colours

        new_palette_image = palette_image.quantize(next_colours, dither = 0)

        # Next step of recursion
        return self.get_recursive_step(new_palette_image, next_colours)
    
    def get_extremal1(self, image: Pim.Image) -> ndarray[Colour]:

        palette_256 = self.get_auto(image, 256)

        # Converts the data to ndarrays
        palette = array([
            array(colour()) for colour in palette_256
        ])
        

        # Finds the most different hue from the median
        median_h = np.median(palette[:, 0]) # Median hue
        extreme_h = max(palette, key = lambda x: abs(x[0] - median_h))
        
        new_palette = self.get_auto(image, self.colours - 1)
        new_palette = np.append(new_palette, Colour(*extreme_h))

        return new_palette

