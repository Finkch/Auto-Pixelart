# A temporal analogue to image

from __future__ import annotations

from image import Image
from palette import Palette
import PIL.Image as Pim
import PIL.ImageSequence as Pis # Well, that's unfortunate naming

class Video:
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

    # Copies the video
    def copy(self, frames: list[Image] = None) -> Video:
        if not frames:
            frames = [image.copy() for image in self.frames]
        
        return Video(
            self.file,
            self.location,
            self.mode,
            frames
        )

    # Setters
    def set_file(self, file: str, location: str = 'inputs') -> None:
        self.file = file
        self.file_name = file[:file.index('.')]
        self.file_extension = file[file.index('.') + 1:]
        
        self.location = location

    # Applies a palette to every frame
    def palettise(self, palette: Palette) -> Video:
        
        # Gets the flattened palette
        colours = list(palette.colours.flatten())

        # Creates an image containing the palette
        palette_image = Pim.new('P', (len(colours), 1))
        palette_image.putpalette(colours)

        # Palettises each frame using the palette image
        frames = [frame.palettise(palette_image) for frame in self.frames]

        return self.copy(frames)
        


