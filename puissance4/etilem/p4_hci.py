# coding: utf-8
# pylint: disable=c0103
"""
module d'interactions utilisateur(s) / programme
HCI = Human-Computer Interactions (Interactions Homme-Machine en français)
"""

from p4_config import SPRITE, WIDTH, HEIGHT

def display(board):
    """
    Affiche la grille
    """
    print()
    print("|", end='')
    for i in range(WIDTH):
        print(f"c{i+1}|", end='')
    print()
    for y in range(HEIGHT):
        print("|", end='')
        for x in range(WIDTH):
            token = board.grille[x][y]
            print(f"{SPRITE[token]} |", end='')
        print()

def say(m):
    """
    Affiche un message
    """
    print("\n", m)
