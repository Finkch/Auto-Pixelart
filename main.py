# A little project to turn images and gifs into pixel art

from input import *
from colour import *
from image import Image

from visualise import show_palette
from logger import logger

from performance import *



def main():

    print('Program start!')

    process = True
    while process:

        # There are four valid modes of operation:
        #   p - process image
        #   v - visualise palette
        #   t - run tests
        #   x - exit
        mode = choose_mode()

        # Beginst the correct mode
        match mode:
            case 'p': process_image()
            case 'v': visualise_palette()
            case 't': test_performance()
            case 'x': break
        
        # Checks if the user wants to continue processing images
        process = choose_continue()


    # Chooses an image to process
    image = Image()
    choose_file(image)

    # Shows the plaette of an image
    show_palette(image, weighted_colour)

    print('Program end!')



# The three menu options

# Processes an image into pixel art
#   TODO
def process_image():
    image = Image()
    choose_file(image)
    choose_palette_size(image)
    choose_resolution(image)

    pim = image.source
    print(pim.format, pim.size, pim.mode)


# Looks at the palette of an image
def visualise_palette():
    image = Image()
    choose_file(image)

    # CHOOSE METHOD OF COMBINING COLOURS

    show_palette(image)
    

# Runs performance tests
#   TODO
def test_performance():
    pass

    

if __name__ == '__main__':
    main()