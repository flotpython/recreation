# coding: utf-8
# pylint: disable=c0111

import random

SPRITE = ' ◉◎'
HUMAN = 1
MACHINE = 2
VOID = 0
WIDTH, HEIGHT = (7, 6)
END = ''

class Board:

    def __init__(self):
        """
        Matrice des jetons
        """
        self.legal_positions = []
        for x in range(WIDTH):
            for y in range(HEIGHT):
                self.legal_positions.append((x, y))
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

    def who_has_won(self):
        """
        Y a-t-il un gagnant ?
        """
        for y in range(HEIGHT):
            for x in range(WIDTH):
                token = self.matrix[x][y]
                if token != VOID and self.find_pattern(x, y) >= 4:
                    return token
        return VOID

    def find_pattern(self, x, y):
        """
        Recherche en étoile pour un jeton de possibles
        segments de jetons contigus
             +  +  +
              + + +
               +++
             +++o+++
               +++
              + + +
             +  +  +
        Renvoit la taille du segment le plus long
        """
        liste = range(-3, 4)
        # directions éligibles / N=north / S=south / W=west / E=east
        directions = {
            'W_to_E': ((i, 0) for i in liste),
            'NW_to_SE': ((i, i) for i in liste),
            'N_to_S': ((0, i) for i in liste),
            'NE_to_SW': ((-i, i) for i in liste),
        }
        token = self.matrix[x][y]
        accumulateur = 0
        for deltas in directions.values():
            stack = maximum = 0
            for i, j in deltas:
                dx, dy = x+i, y+j
                if (dx, dy) in self.legal_positions and self.matrix[dx][dy] == token:
                    stack += 1
                else:
                    stack = 0
                maximum = max(stack, maximum) # taille du + long segment trouvé dans cette direction
            accumulateur = max(maximum, accumulateur)
        return accumulateur # taille du + long segment trouvé dans toutes les directions

board = Board()
player = HUMAN
while board.who_has_won() == VOID:
    if board.drop_token(player, random.randint(1, 7)):
        player = 3 - player # alterne HUMAN / MACHINE
    board.display()
print(f"\n{SPRITE[board.who_has_won()]} a gagné !")
