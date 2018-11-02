# coding: utf-8
# pylint: disable=c0103,r0903
"""
module de joueur
"""

from random import choice

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

class Random(Player):

    def __init__(self):
        Player.__init__(self)

    def play(self, board):
        return choice(list(board.playable_cases()))

class IA(Player):

    def __init__(self):
        Player.__init__(self)
