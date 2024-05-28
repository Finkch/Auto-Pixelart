# Reads files and images

from os import listdir

# Returns a list of images present in the input directory
def report_images():

    # Gets a list of files
    files = listdir('PUT IMAGES HERE')
    
    # Formats the list into a presentable string
    out = [f'[{i + 1}]\t{files[i]}' for i in range(len(files))]

    return out