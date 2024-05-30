# Class that represents an image
# This class contains PIL.Image

from PIL import Image as Pim

class Image():
    def __init__(self) -> None:
        self.file           = None
        self.palette_size   = None
        self.width          = None

        self.source         = None

        self.colours        = None

        self.height         = 0 # TODO


    # A few setters
    def set_file(self, file: str) -> None:
        self.file = file
        self.path = f'PUT IMAGES HERE/{file}'

        self.source = Pim.open(self.path)

    def set_palette_size(self, size: int | str) -> None:
        if size in 'd':
            self.palette_size = 8
        elif size in 'a':
            self.palette_size = 1 # TODO
        else:
            self.palette_size = int(size)

    def set_resolution(self, width: int | str) -> None:
        self.width = int(width)

        self.height = 0 # TODO

    
    # Brings some PIL.Image methods up to this class
    def get_colours(self):

        # PIL.Image takes max_colours as an argument
        return self.source.getcolors(self.source.height * self.source.width)