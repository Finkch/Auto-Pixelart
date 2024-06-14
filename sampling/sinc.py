
from image import Image
from PIL.Image import LANCZOS

# Using PIL's resizing method
def sinc_pil(input: Image, output: Image, log = False):
    output.source = input.source.resize((output.width, output.height), resample = LANCZOS)
    return output