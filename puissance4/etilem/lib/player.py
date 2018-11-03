# coding: utf-8
# pylint: disable=c0103,r0903,r0201
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
    """
    Joueur interactif (utilisateur)
    """
    def __init__(self):
        Player.__init__(self)

    def play(self, game):
        """
        Joue une case candidate
        """
        columns = list((x+1 for x, _ in game.board.playable_cases()))
        col = 0
        while col not in columns:
            try:
                col = int(input(game.say('choice')))
            except ValueError:
                print(game.say('invalid'))
        for x, y in game.board.playable_cases():
            if x == col-1:
                return x, y

class Random(Player):
    """
    Joueur machine jouant au hasard
    """
    def __init__(self):
        Player.__init__(self)

    def play(self, game):
        """
        Joue une case candidate
        """
        return choice(list(game.board.playable_cases()))

class AI(Player):
    """
    Joueur IA
    """
    def __init__(self):
        Player.__init__(self)
