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
        self.dropped = 0 # nombre de jetons présents dans la grille
        self.search_calls = 0 # compteur d'appels de la méthode de recherche

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

    def play(self, player, column):
        x = column - 1
        for y in reversed(range(HEIGHT)):
            if self.grille[x][y] == VOID:
                self.grille[x][y] = player
                self.dropped += 1
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
        self.search_calls += 1
        if n == 0: # amplitude de recherche, si nul, segment de longeur n trouvé
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
        board.display()
        print("\nEgalité !")
        break
    col = random.randint(1, WIDTH)
    if board.play(c_player, col):
        if board.has_won(c_player):
            board.display()
            print(f"\n{SPRITE[c_player]}  a joué c{col} et gagne !")
            break
        c_player = switch(c_player)

print()
print(f"Longueur du segment recherché : {LENGTH}")
print(f"Appels de la fonction de recherche : {board.search_calls}")
