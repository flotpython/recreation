# coding: utf-8
# pylint: disable=c0103
"""
module de classe du jeu
"""

from p4_search import solved

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
        Modifie la grille suivant la colonne jouée par le joueur courant
        Renvoit True si le coup est acté, False si la colonne était pleine
        """
        x = column - 1
        for y in reversed(range(self.board.height)):
            if self.board.is_playable((x, y)):
                self.board.grille[x][y] = self.player.code
                self.board.dropped += 1
                return True
        return False

    def has_winner(self):
        """
        Teste si le joueur courant a gagné la partie
        """
        return solved(self.board, self.player, self.length)

    def next_move(self):
        """
        Définit le joueur suivant
        """
        if self.board.dropped > 0:
            self.players.reverse()
        self.player = self.players[0]
