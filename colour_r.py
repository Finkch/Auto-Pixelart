# Contains an object to represent colour

from numpy import ndarray

class ColourList:
    def __init__(self, image_colours: ndarray) -> None:
        self.data           = image_colours
        self.colours        = image_colours[:, 1]
        self.frequencies    = image_colours[:, 0]

    # Returns colour data
    def __call__(self) -> ndarray:
        return self.colours
    
    # Given a tuple of colour, returns the most similar
    # that exists in the ColourList
    def similar(self, colour: tuple) -> tuple:
        return min(self.colours, key = lambda c: sum([
                (c[0] - colour[0]) ** 2,
                (c[1] - colour[1]) ** 2,
                (c[2] - colour[2]) ** 2
            ])
        )

