# Tracks colour and colour operations

from image import Image
import threading
from os import cpu_count

from time import process_time as clock

class Colour:
    def __init__(self, R: int = 0, G: int = 0, B: int = 0):
        self.R = R
        self.G = G
        self.B = B



# Below are a few functions to count the colours in an image
#   For some reason, the serial method is about twice as fast
#   Too much overhead, too small data size?

# Returns a list of 
def count_colours_serial(image: Image) -> dict:

    # Contains colour counts
    #   key:    (R, G, B) as a tuple of integers
    #   value:  integer count
    counts = {}

    i = 0

    # Get data returns an iterable of tuples
    for colour in image.source.getdata():

        # Adds key to the dictionary if it isn't present
        if colour not in counts:
            counts[colour] = 0

        # Increments the count of that colour
        counts[colour] += 1

        i += 1

    return counts


def count_colours_two(image: Image):
    data = list(image.source.getdata())

    chunk1 = data[0 : int(len(data) / 2)]
    chunk2 = data[int(len(data) / 2) : -1]

    results1 = {}
    results2 = {}

    thread1 = threading.Thread(
                target = thread_process_chunk,
                args = (chunk1, results1)
                )
    thread2 = threading.Thread(
                target = thread_process_chunk,
                args = (chunk2, results2)
                )
    thread1.start()
    thread2.start()
    
    thread1.join()
    thread2.join()

    results = {}

    # for result in results1:
    #     if result not in results:
    #         results[result] = 0
    #     results[result] += results1[result]

    # for result in results2:
    #     if result not in results:
    #         results[result] = 0
    #     results[result] += results2[result]
    
    return results

# Counts each colour in the image
def count_colours_parallel(image: Image, thread_count = None) -> dict:
    thread_counts = {}
    counts = {}
    threads = []

    # Uses a number of threads equal(-ish) to the number of cores
    # Makes sure its an even amount of threads
    if thread_count == None:
        thread_count = (cpu_count() // 2) * 2
    
    chunk_size = int(image.source.size[0] * image.source.size[1] / thread_count)

    # Gets the source data for easy reference
    data = list(image.source.getdata())

    # Creates threads to count the colours
    for i in range(thread_count):

        # What an indiviual thread counts
        thread_counts[i] = {}

        # Creates the thread
        # thread = threading.Thread(
        #             target = thread_process_stride,
        #             args = (data, thread_counts[i], i, image.source.size, thread_count)
        #             )
        

        chunk = data[i * chunk_size: i * chunk_size + chunk_size]
        
        thread = threading.Thread(
                        target = thread_process_chunk,
                        args = (chunk, thread_counts[i])
                        )
        
        # Sends the thread on its way
        thread.start()
        threads.append(thread)

    # Waits for all threads to finish
    for thread in threads:
        thread.join()



    # Joins all the results together
    # This is serial! It could probably be improved
    for tid in thread_counts:
        for count in thread_counts[tid]:

            # Adds the key to counts
            if count not in counts:
                counts[count] = 0

            # Adds the value
            counts[count] += thread_counts[tid][count]

    return counts



# Counting colours for one thread
def thread_process_stride(data, results, tid, size, thread_count):

    start = clock()

    # Gets the dimensions of the image so the ending point int known
    pixels = size[0] * size[1]

    # Goes over the pixels assigned to this thread
    for i in range(int(pixels / thread_count)):

        # Gets a pixel's colour
        colour = data[tid + i * thread_count]

        # Adds the colour to the dictionary
        if colour not in results:
            results[colour] = 0
        
        # Counts the colour
        results[colour] += 1


# Counting colours for one thread
def thread_process_chunk(chunk, results):

    # Goes over the pixels assigned to this thread
    for colour in chunk:

        # Adds the colour to the dictionary
        if colour not in results:
            results[colour] = 0
        
        # Counts the colour
        results[colour] += 1
