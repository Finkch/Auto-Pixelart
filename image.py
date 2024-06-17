# Class that represents an image
# This class contains PIL.Image

from PIL import Image as Pim
from PIL.Image import NEAREST, LANCZOS
from colour import Colour
from palette import Palette
from numpy import array, ndarray

class Image():
    def __init__(self, file: str, location: str = 'inputs', size: tuple = None, colours: int = None, HSV: bool = False, palette: str = None, palette_mode: str = 'k') -> None:
        self.file           = None
        self.palette_size   = None
        self.width          = None
        self.height         = None

        self.source         = None

        self.colours        = None
        self.palette        = None
        self.palette_mode   = palette_mode

        self.is_HSV         = HSV

        mode = 'HSV' if self.is_HSV else 'RGB'

        if not file:
            return

        self.set_palette_size(colours)
        self.load(file, location, size, mode)

        if palette:
            self.set_palette(palette, colours)


    # Loads an image from a file
    def load(self, file: str, location: str, size: tuple, mode: str = 'RGB') -> None:
        self.set_file(file, location)
        
        # Creates the source image
        if location == 'inputs':
            self.set(Pim.open(self.path))
        else:
            self.set_resolution(size)
            colour = 'blue' if self.is_HSV else 'white'
            self.source = Pim.new(mode, self.size, color = colour)

    # Sets source to be a PIL image
    def set(self, image: Pim.Image) -> None:
        self.source = image
        self.set_resolution(self.source.size)
        self.colours = self.get_colours()

        if self.palette_size > 0:
            self.palette = self.get_palette()


    # A few setters
    def set_file(self, file: str, location: str) -> None:
        self.file = file
        self.file_name = file[:file.index('.')]
        self.file_extension = file[file.index('.') + 1:]
        self.location = location
        self.path = f'{self.location}/{self.file}'

    def set_resolution(self, size: tuple) -> None:
        if size:
            self.size   = size
            self.width  = size[0]
            self.height = size[1]
        else:
            self.size   = self.source.size
            self.width  = self.size[0]
            self.height = self.size[1]

    def set_palette_size(self, size: int | str) -> None:
        if not size or size == 'd':
            self.palette_size = 8
        elif size == 'a':
            self.palette_size = 1 # TODO
        else:
            self.palette_size = int(size)

    def set_palette(self, palette: str, colours: int = 8) -> None:
        self.palette = Palette(Pim.open(palette), colours = colours)
        self.palette_size = self.palette.colours

    # Updates the name and path
    def update_name(self, name: str, extension: str = None) -> None:
        if extension:
            self.file_extension = extension

        self.file_name = name
        self.file = f'{self.file_name}.{self.file_extension}'
        self.path = f'{self.location}/{self.file}'

    # Updates size to match its source.
    # Yes, this is the same as set_resultion with no supplied
    # arguments, but this convention is more clear.
    def update_size(self) -> None:
        self.set_resolution(None)

    # Gets the scaled size of the source.
    #   If absolute, then `scale` will match the width (preserving aspect ratio).
    #   Otherwise, decrease size by a factor of `scale`.
    def get_size(self, scale: int | float = None, absolute: bool = True) -> tuple:
        if not scale or scale <= 0:
            return self.size
        
        if absolute:
            return scale, int(scale / self.width * self.height)
        else:
            return int(self.width / scale), int(self.height / scale)
        
    # Scales source to given size.
    # Valid choices for method inlcude `n` = `NEAREST` and `s` `SINC/LANCZOS`
    def resize(self, scale: int | float, absolute: bool = True, method: int = 'n') -> None:
        if not self.file:
            return
        
        match method:
            case 'n': method = NEAREST
            case 's': method = LANCZOS
            case _:   ValueError(f'Unknown resampling method "{method}"')

        self.source = self.source.resize(self.get_size(scale, absolute), resample = method)
        self.update_size()
    

    # Saves the source image
    def save(self) -> None:
        if not self.file:
            return

        if not self.source:
            raise ReferenceError('Cannot save image because image source does not exist.')
        
        if self.is_HSV:
            self.source = self.source.convert('RGB')
        self.source.save(self.path)


    # Gets a list of the image's colours
    def get_colours(self, use_HSV: bool = None) -> ndarray:

        # Use RGB or HSV.
        # Prioritises passes arguments.
        HSV = use_HSV
        if use_HSV == None:
            HSV = self.is_HSV

        # If colours already exist, return them.
        # Pah, I can't check if it's None because numpy arrays
        # find that ambiguous, but I can't any() it because None
        # isn't iterable - it's a catch 22. Hence this weird solution.
        #   Cheers to:
        #   https://stackoverflow.com/questions/41928835/how-to-access-the-nonetype-type
        if not isinstance(self.colours, type(None)):
            return array([colour.copy(HSV) for colour in self.colours])

        # PIL.Image takes max_colours as an argument
        cols = self.source.getcolors(self.width * self.height)

        match self.source.mode:
            case 'RGB':
                colours = array([Colour(*frequency_colour[1], frequency = frequency_colour[0], use_HSV = HSV) for frequency_colour in cols])
            case 'P':
                colours = None
            case _:
                ValueError(f'Invalid image mode "{self.source.mode}"')

        return colours
    
    # Returns the RGB/HSV for the chosen palette
    def get_palette(self, use_HSV: bool = None, mode: str = None) -> Palette:

        # Use RGB or HSV.
        # Prioritises passes arguments.
        HSV = use_HSV
        if use_HSV == None:
            HSV = self.is_HSV

        if not mode:
            mode = self.palette_mode

        # Returns existing palette, if there is one
        if self.palette:
            return self.palette.copy(HSV, mode)

        palette = Palette(self.source, self.palette_size, HSV, mode)
        return palette
        
        