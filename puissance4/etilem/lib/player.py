# coding: utf-8
# pylint: disable=c0103
"""
module de joueur
"""

from .config import SPRITE

class Player:
    """
    Joueur, humain ou machine
    """

    def __init__(self, code):
        self.code = code

    def __str__(self):
        return SPRITE[self.code]
