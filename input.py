# Reads files and images

from os import listdir

# Obtains user's choice for file to process
def choose_file(file):

    # Obtains a list of files in the input directory
    files = listdir('PUT IMAGES HERE')

    # Obtains user's choice
    choice = prompt(
        preamble        = 'Choose a file to turn into pixel art:',
        valid_choices   = [str(i + 1) for i in range(len(files))],
        prompts         = [f'[{i + 1}]\t{files[i]}' for i in range(len(files))]
        )

    # Returns the file choses
    return files[int(choice) - 1]


# Prompts user for desired number of colours in the palette
def choose_palette_size(file):

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



# Prompts user for desired resolution of pixel art
def choose_resolution(file):
    
    preamble = 'Choose the pixel width (note that aspect ratio will be preserved):'

    valid_choices = [str(i) for i in range(1, 2049)]

    prompts = [' - \t Enter a number from 1 to 2048']

    choice = prompt(preamble, valid_choices, prompts)

    return choice


# Prompts user for whether to process another image
def choose_continue(file):
    
    preamble = 'Process another file?'

    valid_choices = ['y', 'n']

    prompts = [
        '[y]\tYes',
        '[n]\tNo'
        ]
    
    choice = prompt(preamble, valid_choices, prompts)

    return choice in 'y'


# Prompts user, repeating prompt until given a valid input
def prompt(preamble, valid_choices, prompts):
    
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
