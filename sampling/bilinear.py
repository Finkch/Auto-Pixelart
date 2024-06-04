# The bilinear sampling algorithm
#   Averages over the four nearest neighbours.
#   First two over the x, then one over the y.

from image import Image
from colour import Colour

from colour import weighted_colour

from PIL.Image import BILINEAR

from logger import logger

# This function is bugged and its output is the same as nearest neighbour
def bilinear(image: Image, pixel_art: Image, log: bool = False) -> Image:

    # Pixel map of the source and downscale
    source_map = image.source.load()
    pixel_map = pixel_art.source.load()

    # Obtains the scaling factor
    #   ! This is a float !
    scale = image.width / pixel_art.width

    # Iterates over all the points in the pixel
    for i in range(pixel_art.width):

        # Gets the correspnding coordinates in the original image of i/x
        # s: source, f: floor, c: ceiling
        si = i * scale
        sif = int(si)
        sir = sif + 1
        

        for j in range(pixel_art.height):
            
            # Coordinates in the j/y
            sj = j * scale
            sjf = int(sj)
            sjr = sjf + 1

            # Averages over the two x's
            x1 = weighted_colour([Colour(source_map[sif, sjf]), Colour(source_map[sir, sjf])], [sir - si, si - sif])
            x2 = weighted_colour([Colour(source_map[sif, sjr]), Colour(source_map[sir, sjr])], [sir - si, si - sif])

            # Average over the averages, i.e. average in the y
            y = weighted_colour([x1, x2], [sjr - sj, sj - sjf])

            # Paints the colour
            pixel_map[i, j] = y.RGB


            if log:
                logger.loga('bilinear', f'[{i}, {j}]:\t{pixel_map[i, j]} <- [{si}-{sif}-{sir}, {sj}-{sjf}-{sjr}]')

    return pixel_art

# Using PIL's resizing method
def bilinear_pil(image: Image, pixel_art: Image, log: bool = False) -> Image:
        pixel_art.source = image.source.resize((pixel_art.width, pixel_art.height), resample = BILINEAR)
        return pixel_art