# A simple sampling algorithm: nearest neighbours
#   Maps the downscaled image to the original image,
#   taking each new pixel to be the closest pixel to
#   that point in the original.

from image import Image

from PIL.Image import NEAREST

from logger import logger

def nearest_neighbour(input: Image, output: Image, log = False) -> Image:
    
    # Pixel map of the source and downscale
    source_map = input.source.load()
    pixel_map = output.source.load()

    # Obtains the scaling factor
    #   ! This is a float !
    scale = input.width / output.width

    # Iterates over all the points in the pixel
    for i in range(output.width):
        for j in range(output.height):

            # Gets the correspnding coordinates in the original image
            si, sj = int(i * scale), int(j * scale)

            # Paints the new image
            pixel_map[i, j] = source_map[si, sj]
            
            # Logs
            if log:
                logger.loga('nearest_neighbour', f'[{i}, {j}]:\t{pixel_map[i, j]} <- [{si}, {sj}]:\t{source_map[si, sj]}')

    return output

# Using PIL's resizing method
def nearest_neighbour_pil(input: Image, output: Image, log = False):
    output.source = input.source.resize((output.width, output.height), resample = NEAREST)
    return output

    
