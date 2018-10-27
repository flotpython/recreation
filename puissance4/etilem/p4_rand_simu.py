# coding: utf-8
# pylint: disable=c0103
"""
simulation aléatoire de partie
"""

from random import randint

from p4_config import HUMAN, MACHINE, WIDTH, LENGTH
from p4_board import Board
from p4_player import Player
from p4_hci import display, say

def players():
    """
    Génère les 2 joueurs
    """
    for player in (HUMAN, MACHINE):
        yield Player(player)

board = Board(players())

def start(player=board.next()):
    """
    Démarre la simulation aléatoire
    """
    while True:
        if board.is_full():
            display(board)
            say("Egalité !")
            break
        col = randint(1, WIDTH)
        if board.update(player, col):
            if board.has_won(player):
                display(board)
                say(f"{player}  a joué c{col} et gagne !")
                break
            player = board.next()

    say(f"Longueur du segment recherché : {LENGTH}")

if __name__ == "__main__":
    start()
