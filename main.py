# A little project to turn images and gifs into pixel art

from image import Image

from visualise import show_colour_wheel, show_3d


# Used to select operation performed when the program is run.
# There are two valid processing modes:
#   p - process image
#   v - visualise palette
process     = 'v'


# What file to process
file        = 'yakul.png'

# Image mode (string).
# Either RGB or HSV.
mode        = 'RGB'

# Width of the pixel art.
# Aspect ratio is preserved.
width       = 128

# Colours in the reduced palette
colours     = 16

# Reduction mode of the palette
palette_mode = 's'




# Runs main processing
def main():

    print('Program start!')

    # Beginst the correct mode
    match process:
        case 'p': process_image()
        case 'v': visualise_palette()
        case _:   raise ValueError(f'No such processing mode as "{process}"')
        

    print('Program end!')



# The three menu options

# Processes an image into pixel art
def process_image():
    
    # Gets the source image
    image = Image(
        file,
        mode = mode
    )

    # Gets the palette of the image
    palette = image.palette().reduce(colours, palette_mode)

    # Converts image to pixel art, using the contrained palette
    output = image.pixelate(width, palette)

    output.save()

    # Informs user
    print('\nImage converted to pixel art!')
    print(f'See `output{output.file}` for your image.\n')


# Looks at the palette of an image
def visualise_palette():
    
    # Selects an image
    image = Image(
        file,
        mode = mode
    )

    # Gets the palette
    palette = image.palette().reduce(colours, palette_mode)

    # Converts image to a palette and the colour distribution
    show_colour_wheel(image, palette)
    show_3d(image, palette)
    

    # Informs user
    print('\nImage converted to palette!')
    print(f'See `outputs` directory for your image.\n')
    
    

if __name__ == '__main__':
    main()