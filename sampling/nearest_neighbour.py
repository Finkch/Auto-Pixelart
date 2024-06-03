# A simple sampling algorithm: nearest neighbours
#   Maps the downscaled image to the original image,
#   taking each new pixel to be the closest pixel to
#   that point in the original.

from image import Image

from PIL.Image import NEAREST

from logger import logger

def nearest_neighbour(image: Image, pixel_art: Image, log = False) -> Image:
    
    # Pixel map of the source and downscale
    source_map = image.source.load()
    pixel_map = pixel_art.source.load()

    # Obtains the scaling factor
    #   ! This is a float !
    scale = image.width / pixel_art.width

    # Iterates over all the points in the pixel
    for i in range(pixel_art.width):
        for j in range(pixel_art.height):

            # Gets the correspnding coordinates in the original image
            si, sj = int(i * scale), int(j * scale)

            # Paints the new image
            pixel_map[i, j] = source_map[si, sj]
            
            # Logs
            if log:
                logger.loga('nearest_neighbour', f'[{i}, {j}]:\t{pixel_map[i, j]} <- [{si}, {sj}]:\t{source_map[si, sj]}')

    return pixel_art

# Using PIL's resizing method
def nearest_neighbour_pil(image: Image, pixel_art: Image, log = False):
    pixel_art.source = image.source.resize((pixel_art.width, pixel_art.height), resample = NEAREST)

    
