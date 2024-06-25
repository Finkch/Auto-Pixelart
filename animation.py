# A temporal analogue to image

from __future__ import annotations

from image import Image
from palette import *
import PIL.Image as Pim
from PIL.Image import NEAREST as N
from PIL.Image import LANCZOS as L
import PIL.ImageSequence as Pis # Well, that's unfortunate naming
from display import display

NEAREST = 'n'
LANCZOS = 'l'

FIRST_FRAME = 'f'
APPEND      = 'a'
EVERY       = 'e'

class Animataion:
    def __init__(self, file: str, location: str = 'inputs', mode: str = 'RGB', source: list = None, duration: int = 100) -> None:

        # Sets path information
        self.set_file(file, location)

        self.mode = mode

        # A list of Images
        self.frames: list[Image] = None

        # Sets the source
        if not source:
            self.frames, self.duration = self.read()
        else:
            self.frames, self.duration = source, duration

        self.width  = self.frames[0].width
        self.height = self.frames[0].height
        self.size   = self.frames[0].size

    def read(self) -> list[Image]:
        match self.file_extension:
            case 'gif': return self.read_gif()
            case _:     raise ValueError(f'Invalid video format "{self.file_extension}"')


    def read_gif(self) -> tuple[list[Image], int]:
        frames: list[Image] = []
        frame_count = 0

        # Opens the gif
        gif = Pim.open(f'{self.location}/{self.file}')

        # Adds each frame as an Image to the list
        for frame in Pis.Iterator(gif):
            frame = frame.convert(self.mode)
            frames.append(Image(f'{self.file_name}_{frame_count}.png', 'outputs', source = frame))
            frame_count += 1

        return frames, frame.info['duration']

    # Copies the animation
    def copy(self, frames: list[Image] = None) -> Animataion:
        if not frames:
            frames = [image.copy() for image in self.frames]
        
        return Animataion(
            self.file,
            self.location,
            self.mode,
            frames,
            self.duration
        )
    
    # Saves the animation
    def save(self, file_name: str = None, location: str = 'outputs') -> None:
        
        # Sets defaults
        if not file_name:
            file_name = self.file_name

        # Converts the source to ensure consistent saving
        frames = [frame.source.convert('RGB') for frame in self.frames]
        frames[0].save(
            fp = f'{location}/{file_name}.gif', # Only supports gifs for now
            save_all = True,
            append_images = frames[1:],
            duration = self.duration,
            loop = 0
        )

    # Shows the animation
    def show(self, title = None):
        if not title:
            title = self.file_name
        display(self, title)

    # Setters
    def set_file(self, file: str, location: str = 'inputs') -> None:
        self.file = file
        self.file_name = file[:file.index('.')]
        self.file_extension = file[file.index('.') + 1:]
        
        self.location = location

    # Converts image types
    def convert(self, mode: str) -> Animataion:
        return Animataion(
            self.file,
            self.location,
            mode,
            [frame.convert(mode) for frame in self.frames],
            self.duration
        )

    # Resizes the animation
    def resize(self, width: int, method: str = NEAREST) -> Animataion:
        return self.copy([frame.resize(width, method) for frame in self.frames])
    
    # Applies a filter to each frame
    def filter(self, filter) -> Animataion:
        return self.copy([frame.filter(filter) for frame in self.frames])

    # Skips frames and increases duration, making for choppier animation
    def skip(self, step: int) -> Animataion:
        return Animataion(
            self.file,
            self.location,
            self.mode,
            self.frames[::step],
            int(self.duration * step)
        )
    
    # Flattens the colours in the image to try and enforce a pit of consistency
    def flatten(self, colours: int = 32) -> Animataion:

        # Forces a max on colours
        colours = min(256, colours)

        # Performs k-means cluster reduction on the first frame
        palette = self.frames[0].palette().reduce(colours, KMEANS)
        return self.palettise(palette)

    # Applies a palette to every frame
    def palettise(self, palette: Palette) -> Animataion:
        
        # Gets the flattened palette
        colours = list(palette.colours.flatten())

        # Creates an image containing the palette
        palette_image = Pim.new('P', (len(colours), 1))
        palette_image.putpalette(colours)

        # Palettises each frame using the palette image
        frames = [frame.palettise(palette_image) for frame in self.frames]

        return self.copy(frames)
    
    # Creates pixel art
    def pixilate(self, width: int, palette: Palette) -> Animataion:

        # Applies the palette to every frame
        anim = self.palettise(palette)

        # Downsizes to turn it into, y'know, pixel art
        anim = anim.resize(width, NEAREST)

        # Returns to the orignal size
        anim = anim.resize(self.width, NEAREST)

        return anim
    
    # Gets the colours from the animation
    def get_colours(self, mode: str = APPEND, *args) -> list:
        match mode:
            case 'f': return self.get_colours_frame(*args)
            case 'a': return self.get_colours_append(*args)
            case 'e': return self.get_colour_every(*args)
            case _:   raise ValueError(f'Invalid colour acquisition mode "{mode}"')

    # Gets colours by looking at a given frame
    def get_colours_frame(self, frame: int = 0) -> list:
        return self.frames[frame].get_colours()

    # Gets colours by adding thinner and thinner slices of temporally
    # adjacent frames.
    #   frame: the central frame of the process.
    #   alpha: the exponential dropoff as distance to the central frame increases.
    #   max_distance: look no further ahead/behind than the max distance.
    #
    #   if alpha is 1, then there is no dropoff.
    #   if alpha is 0, then only consider the central frame
    #   if max_distance is -1, then look over all frames.
    def get_colours_append(self, frame: int = 0,  alpha: float = 0.5, max_distance: int = -1) -> list:
        
        # Base cases
        if alpha == 0 or max_distance == 0:
            return self.get_colours_frame(frame)

        # Gets the sources to speed up the process
        frames = [frame.source for frame in self.frames]

        # Gets the base frame
        collage = frames[frame].copy()
        base_width   = collage.width
        base_height  = collage.height

        # Sets default value
        if max_distance == -1:
            max_distance = len(self.frames)

        # Iterates over the set of frames
        for i in range(max(0, frame - max_distance), min(len(self.frames), frame + max_distance)):

            # Calculates the distance, thus the scaling factor
            d = abs(frame - i)
            s = alpha ** d

            # Calculates the width
            swidth = int(base_width * s)

            # Two cases where we should not append the image.
            #   Don't append the central frame, since we already have that.
            #   If the scaled with is negligable, just go to the next iteration.
            if i == frame or swidth == 0:
                continue

            # Scales the image
            simage = frames[i].resize((swidth, base_height))

            # Creates new image
            step = Pim.new(self.mode, (collage.width + swidth, base_height))
            
            # Pastes the two images in, making a collage
            step.paste(collage, (0, 0))
            step.paste(simage,  (collage.width, 0))

            # Updates the collage
            collage = step

        # Returns the collage's colours
        return collage.getcolors(collage.width * collage.height)


    # Gets colour by making a collage of every frame
    def get_colour_every(self) -> list:
        return self.get_colours_append(0, 1, -1)
    
    # Getters
    def colours(self, mode: str = APPEND, *args) -> ColourList:
        return ColourList(self.get_colours(mode, *args), self.mode)
    
    def palette(self, mode: str = APPEND, *args) -> Palette:
        return Palette(self.get_colours(mode, *args), self.mode)



        


