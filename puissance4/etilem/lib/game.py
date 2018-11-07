# coding: utf-8
"""
module de classe du jeu
"""

from itertools import cycle

from .contrib.search import has_won
from .sprite import Sprite
from .player import Human
from .inter import Phrases

class Game:
    """
    Jeu
    """
    def __init__(self, board, players, length, locale):
        """
        Accueille une grille et les 2 joueurs et leur attribue une couleur
        """
        self.locale = locale
        self.say = Phrases(self.locale)
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

    def get_opponent(self):
        """
        Renvoit le joueur s'opposant au joueur courant
        """
        opp = next(self.players)
        if opp == self.player:
            return next(self.players)
        return opp
