#!/usr/bin/env python3
# coding: utf-8
# pylint: disable=c0103,r0903
"""
simulation aléatoire de partie
"""

from lib import Game, Board, Random, WIDTH, HEIGHT, LENGTH

length = LENGTH
game = Game(Board(WIDTH, HEIGHT), (Random(), Random()), LENGTH, "fr")

def start():
    """
    Démarre la simulation interactive
    """
    while True:
        print(game.board)
        if game.board.is_full():
            print(game.say('deuce'))
            break
        case = game.player.play(game)
        game.update(case)
        if game.has_winner():
            print(game.board)
            x, _ = case
            print(game.say('has_played', game.player, f"c{x+1}"), game.say('has_won'))
            break
        game.next_move()

    print(f"\nLongueur du segment recherché : {length}")

if __name__ == "__main__":
    start()
