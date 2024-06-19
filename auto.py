# This file is an alternative entry point for the program.
# Whereas main runs user-friendly menus, auto is a single
# command line set of arguments.

from sys import argv
from image import Image
from visualise import show_colour_wheel, show_3d

# Runs the program.
#   arg[0]: input file name with extensions
#
# Optional parameters:
#   --d: [d]ownscaling algorithm
#   --w: [w]idth of pixel art image
#   --p: number of colours in the [p]alette
#   --u: resolution to [u]pscale to
def auto(args: list, kwargs: dict) -> None:
    
    # Sets defaults and gets optional parameters
    mode = 'p'
    if 'm' in kwargs:
        mode = kwargs['m']

    width = 64
    if 'w' in kwargs:
        width = int(kwargs['w'])

    colours = 8
    if 'c' in kwargs:
        colours = int(kwargs['c'])

    palette_mode = 's'
    if 'p' in kwargs:
        palette_mode = kwargs['p']


    # Obtains input image and palette
    image: Image    = Image(args[0])
    palette = image.palette().reduce(colours, palette_mode)

    match mode:

        # Processes the image
        case 'p':
            image.pixelate(width, palette).save()

        # Shows colours or palette
        case 'v':
            show_colour_wheel(image, palette)
            show_3d(image, palette)


# Reads argv as a list, grabbing arguments
# and key-word arguments.
def read_arguments(args: list) -> tuple[list, dict]:
    
    largs = []
    kwargs = {}

    # Read every item
    while len(args) > 0:

        # Looks for key-word
        if '--' in args[0]:
            kwargs[args[0][2:]] = args[ 1]
            args = args[2:]
        
        # Regular argument
        else:
            largs.append(args[0])
            args = args[1:]
    
    return largs, kwargs


# Runs main
if __name__ == '__main__':

    # We remove the file name - don't need it
    auto(*read_arguments(argv[1:]))