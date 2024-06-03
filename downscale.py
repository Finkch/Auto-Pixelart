# This file downscales images

from input import choose_palette_size

from image import Image
from typing import Callable

def downscale(image: Image, mode: str) -> None:

    # Gets the function associated with the mode
    downscaler = get_downscaler(image, mode)


# Returns the function associated with the mode
def get_downscaler(image: Image, mode: str) -> Callable:

    # The array contains a list of modes that purely downscale
    # Thus we can't impose palette constraints
    if mode not in ['n', 'l', 'c', 's']:
        choose_palette_size(image)

    # Finds the associated function
    match mode:
        case 'n':
            pass
        case 'l':   # NYI, not yet implemented
            pass
        case 'c':   # NYI
            pass
        case 's':   # NYI
            pass
        case _:
            raise ValueError(f'No such downscaling case as "{mode}"') 
