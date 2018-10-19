# coding: utf-8
# pylint: disable=c0111

import random

SPRITE = '◉◎ '
WHITE = HUMAN = 0
BLACK = MACHINE = 1
VOID = 2
WIDTH, HEIGHT = (7, 6)
END = ''

class Board:

    def __init__(self):
        """
        Matrice des jetons
        """
        self.matrix = [[VOID for y in range(HEIGHT)] for x in range(WIDTH)]


    def drop_token(self, player, col):
        """
        Le joueur courant avait-il le droit de jouer dans cette colonne ?
        """
        x = col - 1
        for y in range(HEIGHT):
            index = HEIGHT-1-y # on commence par le bas du tableau
            if self.matrix[x][index] == VOID:
                self.matrix[x][index] = player
                return True
        return False

    def display(self):
        """
        Affiche le tableau des jetons
        """
        print()
        print('|', end=END)
        for i in range(WIDTH):
            print(f"c{i+1}|", end=END)
        print()
        for y in range(HEIGHT):
            print('|', end=END)
            for x in range(WIDTH):
                print(f"{SPRITE[self.matrix[x][y]]} |", end=END)
            print()

    def who_has_win(self):
        """
        Y a-t-il un gagnant ?
        """
        for y in range(HEIGHT):
            for x in range(WIDTH):
                token = self.matrix[x][y]
                if self.find_pattern(x, y) >= 4 and token != VOID:
                    return token
        return VOID

    def find_pattern(self, x, y):
        """
        Recherche en étoile pour un jeton d'une possible
        combinaison de jetons se suivant dans une direction
             +  +  +
              + + +
               +++
             +++o+++
               +++
              + + +
             +  +  +
        Renvoit le plus fort accumulateur de jetons se suivant
        """
        # directions éligibles / N=north / S=south / W=west / E=east
        directions = {
            'W_to_E': ((-3, 0), (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0), (3, 0)),
            'NW_to_SE': ((-3, -3), (-2, -2), (-1, -1), (0, 0), (1, 1), (2, 2), (3, 3)),
            'N_to_S': ((0, -3), (0, -2), (0, -1), (0, 0), (0, 1), (0, 2), (0, 3)),
            'NE_to_SW': ((3, -3), (2, -2), (1, -1), (0, 0), (-1, 1), (-2, 2), (-3, 3)),
        }

        token = self.matrix[x][y]
        accumulateur = 0

        for deltas in directions.values():
            stack = maximum = 0
            for dx, dy in deltas:
                try:
                    if self.matrix[x+dx][y+dy] == token:
                        stack = stack + 1 # on empile les jetons successifs
                        maximum = max(stack, maximum)
                    else:
                        stack = 0 # on vide la pile
                except IndexError:
                    stack = 0
            accumulateur = max(maximum, accumulateur)
        return accumulateur

board = Board()
player = HUMAN
while board.who_has_win() == VOID:
    if board.drop_token(player, random.randint(1, 7)):
        player = 1 - player # alterne HUMAN / MACHINE
    board.display()
print(f"\n{SPRITE[board.who_has_win()]} a gagné !")
