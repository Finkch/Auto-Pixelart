# This file downscales images

from input import choose_palette_size, choose_resolution

from image import Image
from typing import Callable

from PIL import Image as Pim

import sampling.bicubic
import sampling.bilinear
import sampling.kmean
import sampling.nearest_neighbour
import sampling.bilinear
import sampling.sinc

# Downscales an image
def downscale(image: Image, mode: str, downscaling_name: str, width: int = None, palette: str = None) -> Image:

    # Creates a new image
    pixel_art = Image()

    # Sets the resolution of the new image
    if not width:
        width = choose_resolution()
    elif width == -1:
        width = image.width
    pixel_art.set_resolution(width, image)

    # Creates the source for the new image
    pixel_art.set_file(f'{image.file_name} ({downscaling_name}).png', inputs = False)
    pixel_art.read(Pim.new(mode = 'RGB', size = (pixel_art.width, pixel_art.height)))


    # Gets the function associated with the mode
    downscaler = get_downscaler(pixel_art, mode, palette)


    # Runs the downscaler
    pixel_art = downscaler(image, pixel_art)
    
    return pixel_art


# Returns the function associated with the mode
def get_downscaler(image: Image, mode: str, palette: str = None) -> Callable:

    # The array contains a list of modes that purely downscale
    # Thus we can't impose palette constraints
    if mode not in ['n', 'l', 'c', 's']:

        if not palette:
            choose_palette_size(image)
        else:
            image.set_palette_size(palette)

    # Finds the associated function
    match mode:
        case 'n':
            return sampling.nearest_neighbour.nearest_neighbour_pil
        case 'l':
            return sampling.bilinear.bilinear_pil
        case 'c':
            return sampling.bicubic.bicubic_pil
        case 's':
            return sampling.sinc.sinc_pil
        case 'k':
            return sampling.kmean.palettised
        case _:
            raise ValueError(f'No such downscaling case as "{mode}"') 
