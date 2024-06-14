# This file is an alternative entry point for the program.
# Whereas main runs user-friendly menus, auto is a single
# command line set of arguments.

from sys import argv
from input import choose_downscale
from image import Image

# Runs the program.
#   arg[0]: input file name with extensions
#
# Optional parameters:
#   'd': [d]ownscaling algorithm
#   'w': [w]idth of pixel art image
#   'p': number of colours in the [p]alette
#   'u': resolution to [u]pscale to
def auto(args: list, kwargs: dict) -> None:
    
    # Sets defaults and gets optional parameters
    method = 'k'
    if 'd' in kwargs:
        method = kwargs['d']

    width = -1
    if 'w' in kwargs:
        width = int(kwargs['w'])

    palette = 8
    if 'p' in kwargs:
        palette = kwargs['p']


    # Gets the downscaler.
    #   Defaults to 'k', k-mean clustering
    downscaler, downscaler_name, need_palette = choose_downscale(method)

    # Obtains input and output images
    input: Image    = Image(args[0])
    output: Image   = Image(
        file        = input.file, 
        location    = 'outputs',
        size        = input.get_size(width),
        colours     = palette
    )

    # Updates the name of the output
    output.update_name(f'{input.file_name} ({downscaler_name})', extension = 'png')

    # Downscales the image
    output = downscaler(input, output)

    # Upscales the image, if specified
    if 'u' in kwargs:
        output.resize(int(kwargs['u']))

    # Saves the image
    output.save()
    print(f'See `{output.path}` for your image.\n')



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