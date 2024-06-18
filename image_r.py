# Encapsulates PIL.Image

from __future__ import annotations

import PIL.Image as Pim
from PIL.Image import NEAREST, LANCZOS
from colour_r import ColourList
from palette_r import Palette

class Image:
    def __init__(self, file: str, location: str = 'inputs', mode: str = 'RGB', source: Pim.Image = None) -> None:
        self.set_file(file, location)

        self.mode   = mode

        if not source:
            self.source = self.read()
        else:
            self.source = source.convert(self.mode)
            

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

    # Makes a deep copy of this Image
    def copy(self, source: Pim.Image = None) -> Image:
        if not source:
            source = self.source.copy()
        
        return Image(
            self.file,
            self.location,
            self.mode,
            source
        )

    # Converts image to a mode
    def convert(self, mode: str) -> Pim.Image:
        return self.source.convert(mode)
    
    # Resizes image.
    # Method can be:
    #   'n': Nearest neighbour
    #   'l': Lanczos/sinc method
    def resize(self, size: tuple, method: str = 'n') -> Image:
        match method:
            case 'n':
                return self.copy(self.source.resize(size, resample = NEAREST))
            case 'l':
                return self.copy(self.source.resize(size, resample = LANCZOS))
            
    # Conforms the source's colours to a palette
    def palettise(self, palette: Palette) -> Image:
        
        # Gets the flattened palette
        colours = list(palette.palette.colours.flatten())

        # Creates an image containing the palette
        palette_image = Pim.new('P', (len(colours), 1))
        palette_image.putpalette(colours)

        # Quantises the source to the palette
        source = self.source.quantize(palette = palette_image, dither = 0)

        return self.copy(source)
    
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
