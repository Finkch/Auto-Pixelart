# A little project to turn images and gifs into pixel art

from input import *
from colour import *
from image import Image
from PIL import Image as Pim

from visualise import show_palette
from logger import logger

from performance import *


from time import process_time as clock

def main():


    print('Program start!')

    test = True

    loc = 'PUT IMAGES HERE/'

    process = True

    # while process:

    #     image = Image()
    #     choose_file(image)
    #     choose_palette_size(image)
    #     choose_resolution(image)

    #     pim = image.source
    #     print(pim.format, pim.size, pim.mode)

    #     process = choose_continue()

    # Chooses an image to process
    image = Image()
    choose_file(image)

    # Runs some tests
    if test:
        pass

    # Shows the plaette of an image
    show_palette(image, weighted_colour)

    print('Program end!')
    
if __name__ == '__main__':
    main()