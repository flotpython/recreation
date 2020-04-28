
from random import choice


class Bag():

    letter_count = {
        #'*': 2,
        'A': 9,  'B': 2, 'C': 2, 'D': 3,
        'E': 15, 'F': 2, 'G': 2, 'H': 2,
        'I': 8,  'J': 1, 'K': 1, 'L': 5,
        'M': 3,  'N': 6, 'O': 6, 'P': 2,
        'Q': 1,  'R': 6, 'S': 6, 'T': 6,
        'U': 6,  'V': 2, 'W': 1, 'X': 1,
        'Y': 1,  'Z': 1,
    }

    def __init__(self):
        self.bag = set(self.letter_count.keys())

    def is_empty(self):
        return len(self.bag) == 0

    def pick_letters(self, count):
        for i in range(count):
            if not self.is_empty():
                letter = choice(list(self.bag))
                self.letter_count[letter] -= 1
                if self.letter_count[letter] == 0:
                    self.bag.discard(letter)
                yield letter
