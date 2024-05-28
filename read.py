# Reads files and images

from os import listdir

# Obtains user's choice for file to process
def choose_file():

    # Obtains a list of files in the input directory
    files = listdir('PUT IMAGES HERE')

    # Gets a list of valid user inputs
    valid_choices = [str(i + 1) for i in range(len(files))]

    # Gets faulty default value to begin while loop
    choice = 'n/a'


    # Gets a valid choice from the user
    while choice not in valid_choices:

        # Prompts the user
        print('Please chooe file to turn into pixel art:')        
        [print(f'[{i + 1}]\t{files[i]}') for i in range(len(files))]

        # Obtains the choice
        choice = input('% ')

    # Returns the file choses
    return files[int(choice) - 1]
