# coding: utf-8
# pylint: disable=c0111

import random

SPRITE = ' ◉◎'
VOID = 0
HUMAN = 1
MACHINE = 2
WIDTH, HEIGHT = 8, 8
LENGTH = 5
END = ''

def switch(player):
    return 3 - player # alterne HUMAN / MACHINE

class Board:

    def __init__(self):
        self.grille = [[VOID for y in range(HEIGHT)] for x in range(WIDTH)]

    def cases(self):
        for x in range(WIDTH):
            for y in range(HEIGHT):
                yield x, y

    def directions(self):
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx or dy: # exclut le cas (0, 0) qui a déjà été testé
                    yield dx, dy

    def is_valid(self, case):
        return case in self.cases()

    def is_full(self):
        for x, y in self.cases():
            if self.grille[x][y] == VOID:
                return False
        return True

    def play(self, player, x):
        for y in reversed(range(HEIGHT)):
            if self.grille[x][y] == VOID:
                self.grille[x][y] = player
                return True
        return False

    def has_won(self, player):
        for x, y in self.cases(): # pour chaque case de la grille
            for direction in self.directions(): # dans les 8 directions
                # recherche d'un segment de longueur LENGTH de jetons appartenant au joueur
                if self.has_n_in_dir(player, x, y, direction, LENGTH):
                    return True
        return False

    def has_n_in_dir(self, player, x, y, direction, n):
        if n == 0: # profondeur de recherche, si nul, segment de longeur LENGTH trouvé
            return True
        if not self.is_valid((x, y)): # case en dehors de la grille
            return False
        if self.grille[x][y] != player: # case vide ou occupée par un jeton adverse
            return False
        dx, dy = direction
        return self.has_n_in_dir(player, x+dx, y+dy, direction, n-1)

    def display(self):
        print()
        print("|", end=END)
        for i in range(WIDTH):
            print(f"c{i+1}|", end=END)
        print()
        for y in range(HEIGHT):
            print("|", end=END)
            for x in range(WIDTH):
                token = self.grille[x][y]
                print(f"{SPRITE[token]} |", end=END)
            print()

board = Board()
c_player = HUMAN
while True:
    if board.is_full():
        print("\nEgalité !")
        break
    if board.play(c_player, random.randint(0, WIDTH-1)):
        board.display()
        if board.has_won(c_player):
            print(f"\n{SPRITE[c_player]} a gagné !")
            break
        c_player = switch(c_player)
print(f"\nLongueur du segment recherché : {LENGTH}")
