# An implementation of the bicubic sampling method.
#   Where as bilinear averages over the 4 nearest
#   neighbours (2x2), bicubic is over 16 nearest
#   neighbours (4x4).

from image import Image

from PIL.Image import BICUBIC

from logger import logger


# Using PIL's resizing method
def bicubic_pil(input: Image, output: Image):
    output.source = input.source.resize((output.width, output.height), resample = BICUBIC)
    return output