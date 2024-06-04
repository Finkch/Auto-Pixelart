
from image import Image
from PIL.Image import LANCZOS

# Using PIL's resizing method
def sinc_pil(image: Image, pixel_art: Image, log = False):
    pixel_art.source = image.source.resize((pixel_art.width, pixel_art.height), resample = LANCZOS)
    return pixel_art