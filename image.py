# Class that represents an image
# This class contains PIL.Image

from PIL import Image as Pim

class Image():
    def __init__(self) -> None:
        self.file           = None
        self.palette_size   = None
        self.width          = None
        self.height         = None

        self.source         = None

        self.colours        = None


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
    def set_resolution(self, width: int | str, source) -> None:
        self.width = int(width)

        # Preserves aspect ratio
        self.height = int(self.width / source.width * source.height)

    # Reads an image into the source attribute
    def read(self, source: str | Pim.Image) -> None:
        if isinstance(source, str):
            self.source = Pim.open(source)
        elif isinstance(source, Pim.Image):
            self.source = source
        else:
            raise ValueError(f'Cannot read type "{type(source)}"')
        self.update()


    # Sets some values, incase the source image has changed
    def update(self) -> None:
        self.width = self.source.width
        self.height = self.source.height

        # PIL.Image takes max_colours as an argument
        self.colours = self.source.getcolors(self.width * self.height)