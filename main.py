# A little project to turn images and gifs into pixel art

from image import Image

from input import *
from visualise import show_colour_wheel
from performance import run_test

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
def process_image():
    
    # Chooses parameters
    file = choose_file()
    width = choose_resolution()
    downscaler, downscaler_name, need_palette = choose_downscale()
    
    palette_size = 'd'
    if need_palette:
        palette_size = choose_palette_size()

    upscale_width = choose_upscale()

    # Creates the input and output images
    input: Image    = Image(file)

    # Defaults to input image's width
    if not width:
        width = input.width

    output: Image   = Image(
        file        = input.file, 
        location    = 'outputs',
        size        = input.get_size(width),
        colours     = palette_size
    )

    # Updates the output image's name
    output.update_name(f'{input.file_name} ({downscaler_name})')
    
    # Runs
    output = downscaler(input, output)

    # Upscales the image
    if upscale_width:
        output.resize(upscale_width)
    
    # Saves the image
    output.save()

    # Informs user
    print('\nImage converted to pixel art!')
    print(f'See `{output.path}` directory for your image.\n')


# Looks at the palette of an image
def visualise_palette():
    
    # Selects an image
    image = Image(choose_file())

    # Chooses method of squashing colours
    # choose_colour, choose_name = choose_averaging()

    # # Gets colour sorting type
    # use_HSV = choose_colour_type()

    # Converts image to a palette
    image = show_colour_wheel(image)

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