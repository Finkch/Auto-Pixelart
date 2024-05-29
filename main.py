# A little project to turn images and gifs into pixel art

from input import *
from colour import *
from image import Image
from PIL import Image as Pim

import statistics

from time import process_time as clock

def main():

    print('Program start!')

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

    image = Image()
    choose_file(image)

    trials = 10
    threads = [1, 2, 4, 8, 16, 32]

    # trials = 10
    # threads = [2]

    ttimes = []
    stimes = []
    ptimes = []

    print_individual = False


    for t in threads:
        for i in range(trials):
            start = clock()
            scounts = count_colours_serial(image)
            end = clock()
            stimes.append(end - start)

            if print_individual:
                print(f'Serial trial {i}:\t{stimes[-1]}')
            
            
    # for t in threads:
    #     for i in range(trials):
    #         start = clock()
    #         tcounts = count_colours_two(image)
    #         end = clock()
    #         ttimes.append(end - start)

    #         if print_individual:
    #           print(f'Thread trial {i}:\t{ttimes[-1]}')

    for t in threads:
        for i in range(trials):
            start = clock()
            pcounts = count_colours_multiprocess(image, t)
            end = clock()
            ptimes.append(end - start)

            if print_individual:
                print(f'Multiprocess trial {i}:\t{ptimes[-1]}')


        print(f'Number of threads: {t}')
        # print(f'Thread time:\t{sum(ttimes) / len(ttimes)} s')
        print(f'Serial time:\t{sum(stimes) / len(stimes)} s')
        print(f'Multiprocess time:\t{sum(ptimes) / len(ptimes)} s')


    # print(tcounts == scounts)
    
if __name__ == '__main__':
    main()