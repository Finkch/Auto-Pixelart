# A little project to turn images and gifs into pixel art

from input import *
from image import Image

def main():

    process = True

    while process:

        image = Image()
        choose_file(image)
        choose_palette_size(image)
        choose_resolution(image)

        pim = image.image
        print(pim.format, pim.size, pim.mode)

        process = choose_continue()

main()