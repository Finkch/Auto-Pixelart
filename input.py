# Gets user input

from os import listdir
from image import Image

from colour import colour_functions, colour_names

from performance import performance_functions, performance_names

from typing import Callable


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
def choose_file(file: Image) -> None:

    # Obtains a list of files in the input directory
    files = listdir('PUT IMAGES HERE')
    files.remove('.DS_Store')

    # Obtains user's choice
    choice = prompt(
        preamble        = 'Choose a file:',
        valid_choices   = [str(i + 1) for i in range(len(files))],
        prompts         = [f'[{i + 1}]\t{files[i]}' for i in range(len(files))]
    )

    # Returns the file choses
    file.set_file(files[int(choice) - 1])


# Prompts user for desired number of colours in the palette
def choose_palette_size(file: Image) -> None:

    preamble = 'Choose a palette size, the number of colours that will be in the pixel art:'

    valid_choices = ['a', 'd']
    valid_choices += [str(i) for i in range(1, 257)]
    
    prompts = [
        '[a]\tAuto',
        '[d]\tDefault, 8 colours',
        ' - \tOr enter an integer from 1 to 256'
    ]

    choice = prompt(preamble, valid_choices, prompts)

    file.set_palette_size(choice)



# Prompts user for desired resolution of pixel art
def choose_resolution(file: Image) -> None:

    choice = prompt(
        preamble        = 'Choose the pixel width (note that aspect ratio will be preserved):', 
        valid_choices   = [str(i) for i in range(1, 2049)], 
        prompts         = [' - \t Enter a number from 1 to 2048']
    )

    file.set_resolution(choice)


# Chooses method of combining pixel colours for visualising an image's palette
def choose_averaging() -> Callable:

    choice = prompt(
        preamble        = 'Choose method of combining pixel colours:',
        valid_choices   = [f'{i + 1}' for i in range(len(colour_names))],
        prompts         = [f' {i + 1}\t{colour_names[i]}' for i in range(len(colour_names))]
    )

    return colour_functions[int(choice) - 1]

# Chooses how many trials to perform
def choose_trials() -> int:
    
    choice = prompt(
        preamble        = 'Choose how many trials to perform:', 
        valid_choices   = range(1, int(1e4) + 1), 
        prompts         = [' - \t Enter a number from 1 to 10000']
    )

    return int(choice)


# Chooses which tests to perform
def choose_test() -> Callable:

    # Obtains a list of files in the input directory

    choice = prompt(
        preamble        = 'Choose which test to run:', 
        valid_choices   = [str(i) for i in range(len(performance_names))], 
        prompts         = [f'[{i + 1}]\t{performance_names[i]}' for i in range(len(performance_names))]
    )

    return performance_functions(int(choice - 1))





# Prompts user for whether to process another image
def choose_continue() -> bool:
    
    preamble = 'Process another file?'

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
