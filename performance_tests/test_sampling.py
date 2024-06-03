# Tests the performance of sampling algorithm implementations

from image import Image

from sampling.nearest_neighbour import nearest_neighbour, nearest_neighbour_pil

def test_nearest_neighbour(trials):
    source = Image()
    source.set_file('Nora.jpg')

    target = Image()
    target.set_resolution(256, source)
    target.set_file(f'performance_test.png', inputs = False)
    target.new()

    args = (source, target)

    return args, [nearest_neighbour, nearest_neighbour_pil], ['Serial', 'PIL'], False