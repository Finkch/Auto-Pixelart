# Tests the performance of sampling algorithm implementations

from image import Image

from sampling.nearest_neighbour import nearest_neighbour, nearest_neighbour_pil
from sampling.bilinear import bilinear, bilinear_pil

# Creates a pair of images to test on
def setup_test():
    source = Image()
    source.set_file('Nora.jpg')

    target = Image()
    target.set_resolution(256, source)
    target.set_file(f'performance_test.png', inputs = False)
    target.new()

    args = (source, target)

    return args


# Nearest neighbour
def test_nearest_neighbour(trials):
    args = setup_test()

    return args, [nearest_neighbour, nearest_neighbour_pil], ['Serial', 'PIL'], False


# Bilinear
def test_bilinear(trials):
    args = setup_test()

    return args, [bilinear, bilinear_pil], ['Serial', 'PIL'], False