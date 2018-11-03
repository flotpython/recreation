# coding: utf-8
# pylint: disable=c0103,r0903
"""
module de classe du jeu
"""

from itertools import cycle

from .inter import Phrases
from .contrib.search import has_won
from .sprite import Sprite
from .player import Human

class Game:
    """
    Jeu
    """
    def __init__(self, board, players, length, locale):
        """
        Accueille une grille et les 2 joueurs et leur attribue une couleur
        """
        self.say = Phrases(locale)
        self.board = board
        for player, color in zip((0, *players), Sprite):
            if player:
                player.code = color
        self.players = cycle(players)
        self.player = next(self.players)
        self.length = length

    def update(self, case):
        """
        Ajoute un jeton dans une case
        """
        self.board.update(case, self.player)
        if not isinstance(self.player, Human):
            x, _ = case
            print(self.say('has_played', self.player, f"c{x+1}"))

    def has_winner(self):
        """
        Teste si le joueur courant a gagné la partie
        """
        return has_won(self.board, self.player, self.length)

    def next_move(self):
        """
        Détermine le joueur suivant
        """
        self.player = next(self.players)
