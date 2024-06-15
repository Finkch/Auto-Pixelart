# Gets user input

from os import listdir

from typing import Callable

from colour import colour_functions, colour_names
from performance import performance_functions, performance_names

import sampling.bicubic
import sampling.bilinear
import sampling.kmean
import sampling.nearest_neighbour
import sampling.bilinear
import sampling.sinc




# Chooses the operational mode
def choose_mode() -> str:

    preamble = "Choose what you would like to do:"

    valid_choices = ['p', 'v', 't', 'x']

    prompts = [
        '[p]\tProcess an image',
        '[v]\tVisualise the palette of an image',
        '[t]\tRun performance tests',
        '[x]\tExit',
    ]

    choice = prompt(preamble, valid_choices, prompts)

    return choice


# Obtains user's choice for file to process
def choose_file() -> str:

    # Obtains a list of files in the input directory
    files = listdir('inputs')
    files.remove('.DS_Store')
    files.remove('.gitignore')

    # Obtains user's choice
    choice = prompt(
        preamble        = 'Choose a file:',
        valid_choices   = [str(i + 1) for i in range(len(files))],
        prompts         = [f'[{i + 1}]\t{files[i]}' for i in range(len(files))]
    )

    # Returns the file choses
    return files[int(choice) - 1]



# Prompts user for desired resolution of pixel art
def choose_resolution() -> int:

    preamble = 'Choose the pixel width (note that aspect ratio will be preserved):'
    
    valid_choices = ['x', 'a', 's', 'd', 'f', 'g', 'h'] + [str(i) for i in range(1, 2049)]
    
    prompts = [
        '[x]\tSame as image resolution',
        '[a]\t8',
        '[s]\t16',
        '[d]\t32',
        '[f]\t64',
        '[g]\t128',
        '[h]\t256',
        ' - \tEnter a number from 1 to 2048'
    ]

    choice = prompt(preamble, valid_choices, prompts)

    # Returns the chosen size
    match choice:
        case 'x': return -1
        case 'a': return 8
        case 's': return 16
        case 'd': return 32
        case 'f': return 64
        case 'g': return 128
        case 'h': return 256
        case _:   return int(choice)

def choose_upscale() -> int:

    preamble = 'Choose width of the upscaled image:'

    valid_choices = ['x', 'a', 's', 'd', 'f', 'g'] + [i + 1 for i in range(4096)]

    prompts = [
        '[x]\tSame as image resolution',
        '[a]\t256',
        '[s]\t512',
        '[d]\t1024',
        '[f]\t2048',
        '[g]\t4096',
        f' -\tEnter a number between 1 and 4096'
    ]

    choice = prompt(preamble, valid_choices, prompts)

    match choice:
        case 'x': return -1
        case 'a': return 256
        case 's': return 512
        case 'd': return 1024
        case 'f': return 2048
        case 'g': return 4096
        case _:   return int(choice)


# Prompts user for the algorithm they want to use
def choose_downscale(choice: str = None) -> tuple[str, str]:

    preamble = 'Choose an algorithm to use:'

    valid_choices = ['n', 'l', 'c', 's', 'k']
    method_names = [
        'Nearest Neighbour',
        'Bilinear',
        'Bicubic',
        'Sinc',
        'k-Means Palette'
    ]

    prompts = [
        '[n]\tNearest Neighbour\t(Downscaling)',
        '[l]\tBilinear\t(Downscaling)',
        '[c]\tBicubic\t(Downscaling)',
        '[s]\tSinc/Lanczos\t(Downscaling)',
        '[k]\tk-Means Palette'
    ]

    if not choice:
        choice = prompt(preamble, valid_choices, prompts)

    if choice not in valid_choices:
        raise ValueError(f'Invalid choice for downsampler: "{choice}"')
    

    downscalers = [
        sampling.nearest_neighbour.nearest_neighbour_pil,
        sampling.bilinear.bilinear_pil,
        sampling.bicubic.bicubic_pil,
        sampling.sinc.sinc_pil,
        sampling.kmean.palettised
    ]

    # Whether or not a palette size needs to be selected
    need_palette = choice in ['k']


    return (
        downscalers[valid_choices.index(choice)], 
        method_names[valid_choices.index(choice)], 
        need_palette
    )


# Prompts user for desired number of colours in the palette
def choose_palette_size() -> str:

    preamble = 'Choose a palette size, the number of colours that will be in the pixel art:'

    valid_choices = ['a', 'd']
    valid_choices += [str(i) for i in range(1, 257)]
    
    prompts = [
        '[a]\tAuto',
        '[d]\tDefault, 8 colours',
        ' - \tOr enter an integer from 1 to 256'
    ]

    choice = prompt(preamble, valid_choices, prompts)

    return choice


# Chooses method of combining pixel colours for visualising an image's palette
def choose_averaging() -> Callable:

    choice = prompt(
        preamble        = 'Choose method of combining pixel colours:',
        valid_choices   = [f'{i + 1}' for i in range(len(colour_names))],
        prompts         = [f'[{i + 1}]\t{colour_names[i]}' for i in range(len(colour_names))]
    )

    return colour_functions[int(choice) - 1], colour_names[int(choice) - 1]

# Chooses whether to use HSV (True) ir RGB (False)
def choose_colour_type() -> bool:
    choice = prompt(
        preamble        = 'Use RGB or HSV to sort:',
        valid_choices   = ['r', 'h'],
        prompts         = ['[r]\tRGB', '[h]\tHSV']
    )

    return 'h' in choice

# Chooses how many trials to perform
def choose_trials() -> int:
    
    choice = prompt(
        preamble        = 'Choose how many trials to perform:', 
        valid_choices   = [str(i) for i in range(1, int(1e4) + 1)], 
        prompts         = [' - \t Enter a number from 1 to 10000']
    )

    return int(choice)


# Chooses which tests to perform
def choose_test() -> Callable:

    # Obtains a list of files in the input directory

    choice = prompt(
        preamble        = 'Choose which test to run:', 
        valid_choices   = [str(i + 1) for i in range(len(performance_names))], 
        prompts         = [f'[{i + 1}]\t{performance_names[i]}' for i in range(len(performance_names))]
    )

    return performance_functions[int(choice) - 1], performance_names[int(choice) - 1]





# Prompts user for whether to process another image
def choose_continue(preamble = 'Process another file?') -> bool:
    
    valid_choices = ['y', 'n']

    prompts = [
        '[y]\tYes',
        '[n]\tNo'
    ]
    
    choice = prompt(preamble, valid_choices, prompts)

    return choice in 'y'


# Prompts user, repeating prompt until given a valid input
def prompt(preamble: str, valid_choices: list[str], prompts: list[str]) -> str:
    
    # Defaults choice to be invalid
    choice = None

    # Loops until given valid choice
    while choice not in valid_choices:

        # Prompts the user
        print(f'\n{preamble}')
        [print(prompt) for prompt in prompts]

        # Obtains user input
        choice = input('% ')

    # Adds an extra new line for good measure
    print()
    
    return choice
