# This file downscales images

from input import choose_palette_size, choose_resolution

from image import Image
from typing import Callable

from PIL import Image as Pim

import sampling
import sampling.bilinear
import sampling.nearest_neighbour

# Downscales an image
def downscale(image: Image, mode: str, downscaling_name: str) -> Image:

    # Creates a new image
    pixel_art = Image()

    # Sets the resolution of the new image
    width = choose_resolution()
    pixel_art.set_resolution(width, image)

    # Creates the source for the new image
    pixel_art.set_file(f'{image.file_name} ({downscaling_name}).png', inputs = False)
    pixel_art.read(Pim.new(mode = 'RGB', size = (pixel_art.width, pixel_art.height)))


    # Gets the function associated with the mode
    downscaler = get_downscaler(pixel_art, mode)


    # Runs the downscaler
    pixel_art = downscaler(image, pixel_art)
    
    return pixel_art


# Returns the function associated with the mode
def get_downscaler(image: Image, mode: str) -> Callable:

    # The array contains a list of modes that purely downscale
    # Thus we can't impose palette constraints
    if mode not in ['n', 'l', 'c', 's']:
        choose_palette_size(image)

    # Finds the associated function
    match mode:
        case 'n':
            return sampling.nearest_neighbour.nearest_neighbour
        case 'l':
            return sampling.bilinear.bilinear
        case 'c':   # NYI
            return None
        case 's':   # NYI
            return None
        case _:
            raise ValueError(f'No such downscaling case as "{mode}"') 
