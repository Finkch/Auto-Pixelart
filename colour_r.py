# Contains an object to represent colour

from numpy import array, ndarray, average

class ColourList:
    def __init__(self, image_colours: list, mode: str = 'RGB') -> None:
        image_colours = array(image_colours)

        self.data           = image_colours
        self.colours        = image_colours[:, 1]
        self.frequencies    = image_colours[:, 0]

        self.mode = mode

    # Returns colour data
    def __call__(self) -> ndarray:
        return self.colours
    
    # Other magic methods
    def __len__(self) -> int:
        return len(self.colours)
    
    # Given a tuple of colour, returns the most similar
    # that exists in the ColourList
    def similar(self, colour: tuple) -> tuple:
        return min(self.colours, key = lambda c: sum([
                (c[0] - colour[0]) ** 2,
                (c[1] - colour[1]) ** 2,
                (c[2] - colour[2]) ** 2
            ])
        )

# Averages colours
def average_colour(colours: ColourList) -> tuple:
    return (

        # Frequency is summed as the new colour would represent
        # a larger portion of the image
        sum(colours.frequencies),
        (
            average(colours.colours[:, 0], colours.frequencies), # Averages each channel
            average(colours.colours[:, 1], colours.frequencies),
            average(colours.colours[:, 2], colours.frequencies),
        )
    )