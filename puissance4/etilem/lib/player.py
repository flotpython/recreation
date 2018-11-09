# coding: utf-8
"""
module de joueur
"""

from random import choice, shuffle

from .contrib.search import has_won
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
        col = 0
        while col not in (x+1 for x, _ in game.board.playable_cases()):
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

    def play(self, game):
        """
        Joue une case candidate
        """
        best = -1000
        best_play = ()
        cases = list(game.board.playable_cases())
        shuffle(cases)
        for case in cases:
            v = self.resolve(game.board, game.player, game.get_opponent(), case, game.length)
            if v > best:
                best = v
                best_play = case
        return best_play

    def resolve(self, board, player, opponent, case, length):
        """
        Renvoit la valeur d'un possible coup
        """
        clone = board.clone()
        clone.update(case, player)
        best = 0
        for l in (x+1 for x in reversed(range(length))):
            if has_won(clone, player, l):
                best += l
                break
        for future in clone.playable_cases():
            final = clone.clone()
            final.update(future, opponent)
            for l in (x+1 for x in reversed(range(length))):
                if has_won(final, opponent, l):
                    best -= l
                    break
        return best
