# Finds and defines palettes

from numpy import array, ndarray
import PIL.Image as Pim
from PIL.Image import NEAREST
from colour import Colour

class Palette:
    def __init__(self, source: Pim.Image, colours: int = 8, HSV: bool = False) -> None:
        self.source = source
        self.colours = colours
        self.HSV = HSV
        self.palette = self.get()

    # Calling a Palette will return an ndarray of values
    def __call__(self) -> ndarray[tuple]:
        return array([colour() for colour in self.palette])


    # Gets best representation for the image's palette.
    # Based on StackOverflow code: https://stackoverflow.com/questions/3241929/how-to-find-the-dominant-most-common-color-in-an-image
    def get(self, dwidth: int = None) -> ndarray[Colour]:

        # Gets a copy of the image to process
        image = self.source.copy()

        # Reduces image size to speed up the computation
        if dwidth:
            dheight = int(dwidth / image.width * image.height)
            image.thumbnail((dwidth, dheight))

        # Reduces the colours in the image.
        # Internally, k-mean clustering is used
        paletted = image.convert('P', palette = Pim.ADAPTIVE, colors = self.colours)
        image_palette = paletted.getpalette()

        # Retrieves a list of dominent colours
        colour_counts = sorted(paletted.getcolors(), reverse = True)

        # Gets the top dominent colours
        palette = []
        for i in range(self.colours):

            # Gets the index of the item
            pindex = colour_counts[i][1]

            # Palette is just a list of values (not tuples), 
            # so we need to stride over items
            palette.append(Colour(*image_palette[pindex * 3 : pindex * 3 + 3], use_HSV = self.HSV))

        return array(palette)
    
    # Saves the palette as an image
    def save(self, file_name: str) -> None:

        # Gets the dimensions of the image
        width   = min(len(self.palette), 16)
        height  = int(len(self.palette) / 16) + 1

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

        # Colours the image to be the 
        for i in range(width):
            for j in range(height):
                pixel_map[i, j] = self.palette[i + j * 16].RGB


        # HSV files cannot be saved, annoyingly
        if self.HSV:
            output = output.convert('RGB')

        # Saves minimum sized image
        output.save(f'palettes/{file_name}.png')

        # Saves a reasonably sized version
        output = output.resize((width * 150, height * 150), resample = NEAREST)
        output.save(f'palettes/{file_name}_large.png')

            
            