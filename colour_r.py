# Contains an object to represent colour

from numpy import array, ndarray, average, round

class ColourList:
    def __init__(self, image_colours: list, mode: str = 'RGB') -> None:

        # We have to do some slight acrobatics here in order to
        # get the colours themselves into a numpy array. If we
        # place the colour arrays directly into data, then because
        # the datatype would be (int, ndarray), it defaults to object
        # and stores the ndarray as a generic object, losing all
        # the advantages of using an array.
        image_colours       = array(image_colours, dtype = object)

        self.data           = image_colours
        self.colours        = array([array(colour[1]) for colour in image_colours])
        self.frequencies    = image_colours[:, 0]

        self.mode = mode

    # Returns colour data
    def __call__(self) -> ndarray:
        return self.colours
    
    # Other magic methods
    def __len__(self) -> int:
        return len(self.colours)
    
    def __getitem__(self, index) -> tuple:
        return self.data[index]
    
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
    return [
        # Frequency is summed as the new colour would represent
        # a larger portion of the image
        sum(colours.frequencies),
        ( # Averages each channel
            int(round(average(colours.colours[:, 0], weights = colours.frequencies))),
            int(round(average(colours.colours[:, 1], weights = colours.frequencies))),
            int(round(average(colours.colours[:, 2], weights = colours.frequencies))),
        )
    ]
# Finds the difference between a pair of colours
def colour_difference_RGB(a: tuple, b: tuple) -> float:
    return sum([
        (a[1][0] - b[1][0]) ** 2,
        (a[1][1] - b[1][1]) ** 2,
        (a[1][2] - b[1][2]) ** 2
    ])

def colour_difference_HSV(a: tuple, b: tuple) -> float:
    return sum([
        (min( # Hue is circular
            abs(a[1][0] - b[1][0]), 
            255 - abs(a[1][0] - b[1][0])
        ) * 2) ** 2,
        (a[1][1] - b[1][1]) ** 2,
        (a[1][2] - b[1][2]) ** 2
    ])

