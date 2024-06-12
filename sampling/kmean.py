from image import Image
from PIL.Image import LANCZOS

# Current implementation:
#   1: Downscale image (sinc) to desired size
#   2: For each pixel, find which in the palette is the closet
#   3: Repaint as closest colour
def palettised(image: Image, pixel_art: Image, log: bool = False) -> Image:
    
    # Downscales the original image
    pixel_art.source = image.source.resize((pixel_art.width, pixel_art.height), resample = LANCZOS)

    # Gets the palette of the image.
    # Halves width to increase performance.
    palette = image.get_palette(pixel_art.palette_size, width = int(image.width / 2))

    