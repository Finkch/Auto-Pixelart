# Tests the creation of a big list of colours.
#   Two implementations are tested, one is a
#   serial conversion and the other uses
#   multiprocessing.

from image import Image

def test_colours(trials):

    # Tests from 1 thread per 8 trails
    # I.e., in trials 24-31 there will be 3 threads
    # args = []
    # for i in range(trials):
    #     args.append([int(i / 8) + 1])

    # Using 4 threads
    # What appears to be the best choice as seen previously
    args = [4]

    # Prepares an image to test on
    image = Image()
    image.set_file('Nora.jpg')

    # Returns the parameters
    return (
        args, 
        [image.get_colours_serial, image.get_colours_parallel, image.baseline_colours], 
        ['Serial', 'Multip', 'Baseline'], 
        False
    )