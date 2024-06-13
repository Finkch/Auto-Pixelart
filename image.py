# Class that represents an image
# This class contains PIL.Image

from PIL import Image as Pim
from colour import Colour
from numpy import array, ndarray

class Image():
    def __init__(self, HSV: bool = False) -> None:
        self.file           = None
        self.palette_size   = None
        self.width          = None
        self.height         = None

        self.source         = None

        self.colours        = None

        self.is_HSV = HSV


    # A few setters
    def set_file(self, file: str, inputs: bool = True) -> None:
        self.file = file
        self.file_name = file[:file.index('.')]
        self.file_extension = file[file.index('.'):]

        # Reads the image if its an input
        # Also sets the path
        if inputs:
            self.path = f'inputs/{file}'
            self.read(self.path)
        else:
            self.path = f'outputs/{file}'

    def set_palette_size(self, size: int | str) -> None:
        if size in 'd':
            self.palette_size = 8
        elif size in 'a':
            self.palette_size = 1 # TODO
        else:
            self.palette_size = int(size)

    # Sets the resolution of this image, based off of a source image
    def set_resolution(self, width: int, source) -> None:
        self.width = width

        # Preserves aspect ratio
        self.height = int(self.width / source.width * source.height)

    # Scale the image using nearest neighbour
    def scale(self, width: int) -> None:
        height = int(width / self.width * self.height)

        self.source = self.source.resize((width, height), resample = Pim.NEAREST)
        self.update()

    # Reads an image into the source attribute
    def read(self, source: str | Pim.Image) -> None:
        if isinstance(source, str):
            self.source = Pim.open(source)
        elif isinstance(source, Pim.Image):
            self.source = source
        else:
            raise ValueError(f'Cannot read type "{type(source)}"')
        self.update()
    
    # Makes a new source image
    def new(self) -> None:
        self.source = Pim.new(mode = 'RGB', size = (self.width, self.height))

    # Saves the source image
    def save(self):
        if not self.source:
            raise ReferenceError('Cannot save image because image source does not exist.')
        
        self.source.save(self.path)


    # Sets some values, incase the source image has changed
    def update(self) -> None:
        self.width = self.source.width
        self.height = self.source.height

        # Updates the colour list
        self.get_colours()


    def get_colours(self) -> None:

        # PIL.Image takes max_colours as an argument
        cols = self.source.getcolors(self.width * self.height)

        match self.source.mode:
            case 'RGB':
                self.colours = [Colour(*frequency_colour[1], frequency = frequency_colour[0], use_HSV = self.is_HSV) for frequency_colour in cols]
            case 'P':
                pass

        return self.colours
    
    # Gets best representation for the image's palette.
    # Based on StackOverflow code: https://stackoverflow.com/questions/3241929/how-to-find-the-dominant-most-common-color-in-an-image
    def get_palette(self, size: int, top: int = None, width: int = None) -> ndarray[Colour]:
        if not top:
            top = size

        # Gets a copy of the image to process
        image = self.source.copy()

        # Reduces image size to speed up the computation
        if width:
            height = int(width / image.width * image.height)
            image.thumbnail((width, height))

        # Reduces the colours in the image.
        # Internally, k-mean clustering is used
        paletted = image.convert('P', palette = Pim.ADAPTIVE, colors = size)
        image_palette = paletted.getpalette()

        # Retrieves a list of dominent colours
        colour_counts = sorted(paletted.getcolors(), reverse = True)

        # Gets the top dominent colours
        palette = []
        for i in range(top):

            # Gets the index of the item
            pindex = colour_counts[i][1]

            # Palette is just a list of values (not tuples), 
            # so we need to stride over items
            palette.append(Colour(*image_palette[pindex * 3 : pindex * 3 + 3], use_HSV = self.is_HSV))

        return array(palette)
        
        