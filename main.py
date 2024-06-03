# A little project to turn images and gifs into pixel art

from image import Image

from input import *
from visualise import show_palette
from performance import run_test
from downscale import downscale

from logger import logger


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


    print('Program end!')



# The three menu options

# Processes an image into pixel art
#   TODO
def process_image():
    image = Image()
    choose_file(image)

    pixel_art = Image()
    width = choose_resolution()
    pixel_art.set_resolution(width, image)

    downscale_mode, downscale_name = choose_downscale()
    

    # Runs
    pixel_art = downscale(image, downscale_mode, downscale_name)



    # Informs user
    print('\nImage converted to pixel art!')
    print(f'See `outputs/{pixel_art.file}` directory for your image.\n')


# Looks at the palette of an image
def visualise_palette():
    
    # Selects an image
    image = Image()
    choose_file(image)

    # Chooses method of squashing colours
    choose_colour, choose_name = choose_averaging()

    # Converts image to a palette
    image = show_palette(image, choose_colour, choose_name)

    # Informs user
    print('\nImage converted to palette!')
    print(f'See `outputs/{image.file}` directory for your image.\n')
    

# Runs performance tests
def test_performance():
    
    # Chooses test to run
    test_funciton, file = choose_test()

    # Chooses number of trails
    trials = choose_trials()

    # Runs the test
    results = run_test(test_funciton, trials)

    # Logs the results
    logger.log(file, results)

    # Informs user
    print('\nTests completed!')
    print(f'See `logs/{file}.txt` directory for performance data.\n')

    

if __name__ == '__main__':
    main()