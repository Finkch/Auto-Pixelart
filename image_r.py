# Encapsulates PIL.Image

import PIL.Image as Pim
from PIL.Image import NEAREST, LANCZOS
from colour_r import ColourList
from palette_r import Palette

class Image:
    def __init__(self, file: str, location: str = 'inputs', mode: str = 'RGB') -> None:
        self.set_file(file, location)

        self.mode   = mode

        self.source = self.read()
            

        self.width  = self.source.width
        self.height = self.source.height
        self.size   = self.source.size

    # Reads an Pim.Image
    def read(self) -> Pim.Image:
        source = Pim.open(f'{self.location}/{self.file}',)
        
        # Ensures the image is in the right mode
        if self.mode != source.mode:
            source = source.convert(self.mode)

        return source
    
    # Saves an image
    def save(self, file_name: str = None, location: str = 'outputs', extension: str = None) -> None:
        
        # Sets defaults
        if not extension:
            extension = self.file_extension
        if not file_name:
            file_name = self.file_name

        self.source.save(f'{location}/{file_name}.{extension}')

    # Converts image to a mode
    def convert(self, mode: str) -> Pim.Image:
        return self.source.convert(mode)
    
    # Resizes image.
    # Method can be:
    #   'n': Nearest neighbour
    #   'l': Lanczos/sinc method
    def resize(self, size: tuple, method: str = 'n') -> Pim.Image:
        match method:
            case 'n':
                return self.source.resize(size, resample = NEAREST)
            case 'l':
                return self.source.resize(size, resample = LANCZOS)

    # Setters
    def set_file(self, file: str, location: str = 'inputs') -> None:
        self.file = file
        self.file_name = file[:file.index('.')]
        self.file_extension = file[file.index('.') + 1:]
        
        self.location = location

    # Getters
    def colours(self) -> ColourList:
        return ColourList(self.source.getcolors(self.width * self.height), self.mode)
    
    def palette(self) -> Palette:
        return Palette(self.colours())