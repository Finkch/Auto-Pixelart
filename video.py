# A temporal analogue to image

from image import Image
import PIL.Image as Pim
import PIL.ImageSequence as Pis # Well, that's unfortunate naming

class Video:
    def __init__(self, file: str, location: str = 'inputs', mode: str = 'RGB') -> None:

        # Sets path information
        self.set_file(file, location)

        self.mode = mode

        # A list of Images
        self.frames: list[Image] = None

    # Setters
    def set_file(self, file: str, location: str = 'inputs') -> None:
        self.file = file
        self.file_name = file[:file.index('.')]
        self.file_extension = file[file.index('.') + 1:]
        
        self.location = location

