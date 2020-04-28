
from .solver import Solver


class Player():

    solver = Solver()

    def __init__(self, name):
        self.name = name
        self.tiles = []
        self.score = 0

    def get_tiles(self):
        return ''.join(self.tiles)

    def fill_tiles(self, bag, max):
        self.tiles.extend(list(bag.pick_letters(max - len(self.tiles))))

    def find_best_move(self, board):
        best_value = 0
        best_move = ()
        for word, vec in self.solver.find_playable_words(self.get_tiles(), board):
            value = board.evaluate(word, vec, self.solver)
            if value > best_value:
                best_value = value
                best_move = (word, vec)
        return best_move, best_value


class Virtual(Player):
    pass


class Computer(Player):
    pass


class Cheater(Player):
    pass


class Human(Player):
    pass
