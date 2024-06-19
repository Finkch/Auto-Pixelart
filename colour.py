# Contains an object to represent colour

from __future__ import annotations

from numpy import array, ndarray, average, round, column_stack
from colorsys import hsv_to_rgb, rgb_to_hsv

from logger import logger

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
    
    # Converts colours to a different mode
    def convert(self, mode: str) -> ColourList:
        if self.mode == mode:
            return ColourList(self.data, mode)
        
        
        # Converts each item to RGB/HSV appropriately.
        # Has to transform from 0-255 to 0-1 amd back up to 0-255.
        # Plus, it has to be an int at the end.
        # The colour array is transformed separately to packing it
        # with frequency because otherwise the data would be in an
        # array of data-type "object", preventing correct casting.
        if self.mode == 'RGB' and mode == 'HSV':
            
            # Transforms colour
            hsv = array(round(
                255 * array(
                    [rgb_to_hsv(*(self.colours[i] / 255)) for i in range(len(self.data))]
                )
            ), dtype=int)            

            return ColourList(
                [( # Packs frequency and colour together
                    self.frequencies[i],
                    hsv[i]
                ) for i in range(len(self.data))],
                mode = mode
            )


        if self.mode == 'HSV' and mode == 'RGB':
            
            # Transforms colour
            rgb = array(round(
                255 * array(
                    [hsv_to_rgb(*(self.colours[i] / 255)) for i in range(len(self.data))]
                )
            ), dtype=int)

            return ColourList(
                [( # Packs frequency and colour together
                    self.frequencies[i],
                    rgb[i]
                ) for i in range(len(self.data))],
                mode = mode
            )

        raise ValueError(f'Cannot convert from mode "{self.mode}" to "{mode}".')
    
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

def colour_difference_H(a: tuple, b: tuple) -> float:
    return min( # Hue is circular
            abs(a[1][0] - b[1][0]), 
            255 - abs(a[1][0] - b[1][0])
        )
