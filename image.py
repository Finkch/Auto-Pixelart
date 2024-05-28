# Class that represents an image
# This class contains PIL.Image

class Image():
    def __init__(self):
        self.file           = None
        self.palette_size   = None
        self.width          = None

        self.colours        = None

        self.height         = 0 # TODO


    # A few setters
    def set_file(self, file):
        self.file = file
        self.path = f'PUT IMAGES HERE/{file}'

    def set_palette_size(self, size):
        if size in 'd':
            self.palette_size = 8
        elif size in 'a':
            self.palette_size = 1 # TODO
        else:
            self.palette_size = size

    def set_resolution(self, width):
        self.width = width

        self.height = 0 # TODO