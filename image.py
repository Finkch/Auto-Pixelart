# Encapsulates PIL.Image

from __future__ import annotations

import PIL.Image as Pim
from PIL.ImageFilter import BLUR, SMOOTH, SMOOTH_MORE, SHARPEN, UnsharpMask, FIND_EDGES
from PIL.Image import NEAREST as N
from PIL.Image import LANCZOS as L
from colour import ColourList, average_colour, colour_difference_HSV, colour_difference_RGB
from palette import Palette

from logger import logger

NEAREST = 'n'
LANCZOS = 'l'

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
    def save(self, file_name: str = None, location: str = 'outputs', extension: str = 'png') -> None:
        
        # Sets defaults
        if not extension:
            extension = self.file_extension
        if not file_name:
            file_name = self.file_name

        # Converts the source to ensure consistent saving
        source = self.source.convert('RGB')
        source.save(f'{location}/{file_name}.{extension}')

    # Shows the image
    def show(self, title: str = None) -> None:
        self.source.show(title)

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
    def convert(self, mode: str) -> Image:
        return Image(
            self.file,
            self.location,
            mode,
            self.source.convert(mode)
        )
    
    
    # Resizes image.
    # Method can be:
    #   'n': Nearest neighbour
    #   'l': Lanczos/sinc method
    def resize(self, width: int, method: str = NEAREST) -> Image:

        # Gets the height that preserves aspect ratio
        height = int(width / self.width * self.height)
        size = (width, height)

        match method:
            case 'n':
                return self.copy(self.source.resize(size, resample = N))
            case 'l':
                return self.copy(self.source.resize(size, resample = L))
            
    # Conforms the source's colours to a palette
    def palettise(self, palette: Palette) -> Image:
        
        # Gets the flattened palette
        colours = list(palette.colours.flatten())

        # Creates an image containing the palette
        palette_image = Pim.new('P', (len(colours), 1))
        palette_image.putpalette(colours)

        # Quantises the source to the palette
        source = self.source.quantize(palette = palette_image, dither = 0)

        return self.copy(source)
    
    # Turns the source image into pixel art
    def pixelate(self, width: int, palette: Palette, denoise: bool = False, *args) -> Image:

        # Constrains the image palette
        image = self.palettise(palette)

        # Downscales to make it, y'know, pixel art
        image = image.resize(width, 'n')

        # Denoises
        if denoise:
            image = image.denoise(*args)

        # Upscales to match original resolution
        image = image.resize(self.width, 'n')

        return image
    
    # Applies a filter to the image.
    # Image filters are imported from PIL.
    def filter(self, filter) -> Image:
        return self.copy(self.source.filter(filter))
    
    # Setters
    def set_file(self, file: str, location: str = 'inputs') -> None:
        self.file = file
        self.file_name = file[:file.index('.')]
        self.file_extension = file[file.index('.') + 1:]
        
        self.location = location

    # Getters
    def get_colours(self) -> tuple:
        if self.mode == 'L':
            colours = self.source.getcolors(self.width * self.height)
            return [(colour[0], [colour[1]] * 3) for colour in colours]
        
        return self.source.getcolors(self.width * self.height)

    def colours(self) -> ColourList:
        return ColourList(self.get_colours(), self.mode)
    
    def palette(self) -> Palette:
        return Palette(self.get_colours(), self.mode)
    

    # Denoises a pixel image.
    # If the difference between a given pixel and the average of
    # its neighbours is less than a threshold, set it to its most
    # dominent neighbour.
    # Threshold is a percent.
    def denoise(self, threshold: float = 60, radius: int = 2) -> Image:

        # Grabs the pixel map
        pixels = self.source.load()

        # Loads new image to 
        output = Pim.new(self.mode, self.size, 'white')
        output_pixels = output.load()

        # Goes over every pixel
        for i in range(self.width):
            for j in range(self.height):
                output_pixels[i, j] = self.denoise_pixel(pixels, i, j, threshold, radius)

        # Returns the denoised image
        return self.copy(output)
    
    # Runs the denoising process for a single pixel
    def denoise_pixel(self, pixels, x: int, y: int, threshold: float, radius: int) -> tuple:

        # Gets the frequency-colour pairs of neighbours
        neighbours = {}
        for i in range(-radius, radius + 1):
            for j in range(-radius, radius + 1):

                # Makes sure not to access pixels that are out of
                # bounds or the current pixel being inspected
                if x + i < 0 or x + i >= self.width:
                    continue
                elif y + j < 0 or y + j >= self.height:
                    continue
                elif x == i and y == j:
                    continue

                # Gets the colour
                colour = pixels[x + i, y + j]
                
                # Updates frequency
                if colour not in neighbours:
                    neighbours[colour] = 0
                neighbours[colour] += 1

        # Reshapes to make ColourList
        colours = ColourList(
            [(item[1], item[0]) for item in neighbours.items()], 
            self.mode
        )

        # Grabs the most dominent colour
        dominent = sorted(colours.data, reverse = True, key = lambda c: c[0])[0]

        # Returns the appropriate colour
        if dominent[0] / ((2 * (radius + 1)) ** 2) * 100 <= threshold:
            return pixels[x, y]
        else:
            return dominent[1]
