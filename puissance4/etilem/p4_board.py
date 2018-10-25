# coding: utf-8
# pylint: disable=c0103
"""
module de grille
"""

from p4_config import VOID, WIDTH, HEIGHT
from p4_search import solved

class Board:
    """
    Grille du jeu
    """
    def __init__(self, players, w=WIDTH, h=HEIGHT):
        """
        Accueille les joueurs et créé une grille vide
        """
        self.players = [p for p in players]
        self.width, self.height = w, h
        self.grille = [[VOID for y in range(self.height)] for x in range(self.width)]

    def cases(self):
        """
        Génère les cases de la grille
        """
        for x in range(self.width):
            for y in range(self.height):
                yield x, y

    def is_valid(self, case):
        """
        Teste si une case appartient à la grille
        """
        return case in self.cases()

    def is_full(self):
        """
        Teste si la grille est pleine
        """
        for x, y in self.cases():
            if self.grille[x][y] == VOID:
                return False
        return True

    def has_won(self, player):
        """
        Teste si le joueur a gagné la partie
        """
        return solved(self, player)

    def update(self, player, column):
        """
        Modifie la grille suivant la colonne jouée par un joueur
        Renvoit True si le coup est acté, False si la colonne était pleine
        """
        x = column - 1
        for y in reversed(range(self.height)):
            if self.grille[x][y] == VOID:
                self.grille[x][y] = player.code
                return True
        return False

    def next(self):
        """
        Renvoit le joueur suivant
        """
        self.players.reverse()
        return self.players[0]
