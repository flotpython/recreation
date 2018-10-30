# coding: utf-8
# pylint: disable=c0103
"""
module de joueur
"""

from .sprite import Sprite

class Player:
    """
    Joueur, humain ou machine
    """

    def __init__(self, code):
        self.code = code

    def __str__(self):
        return Sprite(self.code).__str__()

class Human(Player):
    def __init__(self):
        Player.__init__(self, Sprite.HUMAN)

class Machine(Player):
    def __init__(self):
        Player.__init__(self, Sprite.MACHINE)

class IA(Machine):
    pass
