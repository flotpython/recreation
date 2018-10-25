# coding: utf-8
# pylint: disable=c0103
"""
simulation aléatoire de partie
"""

from random import randint

from p4_config import HUMAN, MACHINE, WIDTH, LENGTH
from p4_board import Board
from p4_player import Player
from p4_search import solved
from p4_hci import display, say

board = Board()
players = [Player(HUMAN), Player(MACHINE)]
c_player = players[0]

def switch_player():
    """
    Alterne les 2 joueurs
    """
    players.reverse()
    return players[0]

while True:
    if board.is_full():
        display(board)
        say("Egalité !")
        break
    col = randint(1, WIDTH)
    if board.update(c_player.code, col):
        if solved(board, c_player.code):
            display(board)
            say(f"{c_player.sprite}  a joué c{col} et gagne !")
            break
        c_player = switch_player()

say(f"Longueur du segment recherché : {LENGTH}")
