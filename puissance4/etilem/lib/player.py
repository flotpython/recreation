# coding: utf-8
# pylint: disable=c0103,r0903
"""
module de joueur
"""

from .sprite import Sprite

class Player():
    """
    Joueur
    """

    def __init__(self, color=Sprite.VOID):
        self.code = color

    def __str__(self):
        return Sprite(self.code).__str__()

class Human(Player):
    def __init__(self):
        Player.__init__(self)

class Machine(Player):
    def __init__(self):
        Player.__init__(self)

class IA(Machine):
    def __init__(self):
        Machine.__init__(self)
