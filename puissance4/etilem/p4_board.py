# coding: utf-8
# pylint: disable=c0103
"""
module de grille
"""

from p4_config import VOID, WIDTH, HEIGHT

class Board:
    """
    Grille du jeu
    """
    def __init__(self, w=WIDTH, h=HEIGHT):
        """
        Créé une grille vide
        """
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

    def update(self, player, column):
        """
        Modifie la grille suivant la colonne jouée par un joueur
        Renvoit True si le coup est acté, False si la colonne était pleine
        """
        x = column - 1
        for y in reversed(range(self.height)):
            if self.grille[x][y] == VOID:
                self.grille[x][y] = player
                return True
        return False
