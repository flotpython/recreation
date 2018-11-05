# coding: utf-8
"""
module de classe sprite
"""

from enum import Enum

class Sprite(Enum):
    """
    Sprite
    """

    VOID = 0
    WHITE = 1
    BLACK = 2

    def __init__(self, code):
        self.sprite = ' ◉◎'
        self.code = code

    def __str__(self):
        return self.sprite[self.code]
