# coding: utf-8
# pylint: disable=c0103
"""
module de classe du jeu
"""

from . import solved

class Game:
    """
    Jeu
    """
    def __init__(self, board, players, length):
        """
        Accueille une grille et les 2 joueurs
        """
        self.board = board
        self.players = players
        self.player = self.players[0]
        self.length = length

    def update(self, column):
        """
        Ajoute un jeton dans une colonne
        Renvoit True si le coup est acté, False si la colonne était pleine
        """
        x = column - 1
        return self.board.update(x, self.player)

    def has_winner(self):
        """
        Teste si le joueur courant a gagné la partie
        """
        return solved(self.board, self.player, self.length)

    def next_move(self):
        """
        Détermine le joueur suivant
        """
        self.players = self.players[::-1]
        self.player = self.players[0]
