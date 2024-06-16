# Finds and defines palettes

from numpy import array, ndarray
import PIL.Image as Pim
from PIL.Image import NEAREST
from colour import Colour

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
    def image(self) -> Pim.Image:

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

        return self.get_auto(image)

    # Gets best representation for the image's palette.
    # Based on StackOverflow code: https://stackoverflow.com/questions/3241929/how-to-find-the-dominant-most-common-color-in-an-image
    def get_auto(self, image: Pim.Image) -> ndarray[Colour]:

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
    
    # Used with palette images
    def from_palette_image(self, source_copy: Pim.Image) -> ndarray[Colour]:
        
        # Gets the colours in the image
        colours = source_copy.getcolors()

        # Updates colour count
        self.colours = len(colours)

        # Gets Colours in the palette
        palette = [Colour(*colour[1]) for colour in colours]

        return array(palette)


