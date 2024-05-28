# Reads files and images

from os import listdir

# Obtains user's choice for file to process
def choose_file():

    # Obtains a list of files in the input directory
    files = listdir('PUT IMAGES HERE')

    # Obtains user's choice
    choice = prompt(
        preamble        = 'Please chooe file to turn into pixel art:',
        valid_choices   = [str(i + 1) for i in range(len(files))],
        prompts         = [f'[{i + 1}]\t{files[i]}' for i in range(len(files))]
        )

    # Returns the file choses
    return files[int(choice) - 1]


# Prompts user for desired number of colours in the palette
def choose_palette_size():
    pass


# Prompts user for desired resolution of pixel art
def choose_resolution():
    pass


# Prompts user for whether to process another image
def choose_continue():
    pass


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
    
    return choice
