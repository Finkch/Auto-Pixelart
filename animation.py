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

    # Skips frames and increases duration, making for choppier animation
    def skip(self, step: int) -> Animataion:
        return Animataion(
            self.file,
            self.location,
            self.mode,
            self.frames[::step],
            int(self.duration * step)
        )

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
    
    # Flattens the colours in the image to try and enforce a pit of consistency
    def flatten(self, colours: int = 32) -> Animataion:

        # Forces a max on colours
        colours = min(256, colours)

        # Performs k-means cluster reduction on the first frame
        palette = self.frames[0].palette().reduce(colours, KMEANS)
        return self.palettise(palette)
        


