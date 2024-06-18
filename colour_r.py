# Contains an object to represent colour

import numpy as np
from numpy import array, ndarray

import PIL.Image as Pim

class ColourList:
    def __init__(self, source: tuple | Pim.Image) -> None:
        if isinstance(source, Pim.Image):
            data = self.colours_from_source(source)
        else:
            data = self.colours_from_ndarray
        
        self.data           = data[0]
        self.colours        = data[1]
        self.frequencies    = data[2]

    # Returns colour data
    def __call__(self) -> ndarray:
        return self.colours

    # Loads colours from a source 
    def colours_from_source(self, source: Pim.Image) -> tuple:
        return self.colours_from_ndarray(array(source.getcolors(np.multiply(*source.size))))
        
    def colours_from_ndarray(self, data: ndarray) -> tuple:
        return data, data[:, 1], data[:, 0]
    
    # Given a tuple of colour, returns the most similar
    # that exists in the ColourList
    def similar(self, colour: tuple) -> tuple:
        return min(self.colours, key = lambda c: sum([
                (c[0] - colour[0]) ** 2,
                (c[1] - colour[1]) ** 2,
                (c[2] - colour[2]) ** 2
            ])
        )

