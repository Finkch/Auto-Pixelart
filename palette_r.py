# A class to represent an image's palette

from __future__ import annotations

from numpy import array, ndarray
from colour_r import ColourList

import PIL.Image as Pim

from logger import logger


class Palette:
    def __init__(self, colours: ColourList) -> None:
        self.palette    = colours

    # Calling a Palette returns its colours
    def __call__(self) -> ndarray:
        return self.palette()
    
    # Other magic methods
    def __len__(self) -> int:
        return len(self.palette)
    
