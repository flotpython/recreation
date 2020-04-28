
import numpy as np
from copy import deepcopy


class Common():

    max_tiles = 7

    letter_score = {
        '*': 0,
        'A': 1,  'B': 3, 'C': 3,  'D': 2,
        'E': 1,  'F': 4, 'G': 2,  'H': 4,
        'I': 1,  'J': 8, 'K': 10, 'L': 1,
        'M': 2,  'N': 1, 'O': 1,  'P': 3,
        'Q': 8,  'R': 1, 'S': 1,  'T': 1,
        'U': 1,  'V': 4, 'W': 10, 'X': 10,
        'Y': 10, 'Z': 10,
    }

    def __init__(self):
        self.cases = np.array([['_' for y in range(self.RANGE)]
                               for x in range(self.RANGE)])

    def __str__(self):
        out = '\n' + '     '
        for i in range(self.RANGE):
            i += 1
            i %= 10
            out += " " + str(i)
        out += "\n"
        for row in range(self.RANGE):
            out += '    ' + chr(65 + row) + ' '
            for col in range(self.RANGE):
                out += self.get_letter(row, col) + ' '
            out += '\n'
        return out

    def coords(self):
        for x in range(self.RANGE):
            for y in range(self.RANGE):
                yield x, y

    def diagonal(self):
        for x, y in self.coords():
            if x == y:
                yield x

    def directions(self):
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if not dx or not dy:
                    yield dx, dy

    def set_letter(self, x, y, letter):
        if (x, y) in self.coords():
            self.cases[x][y] = letter
        else:
            raise IndexError

    def get_letter(self, x, y):
        if (x, y) in self.coords():
            return self.cases[x][y]
        else:
            raise IndexError

    def is_free(self, x, y):
        return self.get_letter(x, y) == '_'

    def is_empty(self):
        for x, y in self.coords():
            if not self.is_free(x, y):
                return False
        return True

    def get_center(self):
        for x, y in self.coords():
            if self.bonus[x][y] == self.ST:
                return x, y

    def get_letter_bonus(self, x, y):
        if (x, y) in self.coords():
            if self.bonus[x][y] == self.LD:
                return 2
            elif self.bonus[x][y] == self.LT:
                return 3
            else:
                return 1

    def get_word_bonus(self, x, y):
        if (x, y) in self.coords():
            if self.bonus[x][y] == self.WD:
                return 2
            elif self.bonus[x][y] == self.WT:
                return 3
            else:
                return 1

    def place(self, word, vec):
        x, y, horiz = vec
        for i, letter in enumerate(word):
            tx, ty = (x, y + i) if horiz else (x + i, y)
            try:
                self.set_letter(tx, ty, letter)
            except IndexError:
                return False
        return True

    def is_scrabble(self, word, vec):
        free = 0
        x, y, horiz = vec
        for i in range(len(word)):
            tx, ty = (x, y + i) if horiz else (x + i, y)
            if self.is_free(tx, ty):
                free += 1
        if len(word) >= free == self.max_tiles:
            return True
        else:
            return False

    def evaluate(self, word, vec, solver):
        score = 0
        x, y, horiz = vec
        for i, letter in enumerate(word):
            base = 0
            coef = 1
            tx, ty = (x, y + i) if horiz else (x + i, y)
            if self.is_free(tx, ty):
                base += self.letter_score[letter] * \
                    self.get_letter_bonus(tx, ty)
                coef *= self.get_word_bonus(tx, ty)
                pos = (tx, ty, horiz)
                crossword = solver.get_crossword(word, vec, pos, self)
                if len(crossword) > 1:
                    for j, cross_letter in enumerate(crossword):
                        base += self.letter_score[cross_letter]
            else:
                base += self.letter_score[letter]
            score += base
        score *= coef
        if self.is_scrabble(word, vec):
            score += 50
        return score

    def get_evenword(self, word, vec):
        virtual = deepcopy(self)
        if virtual.place(word, vec):
            x, y, horiz = vec
            hdir = ((0, -1), (0, 1))
            vdir = ((-1, 0), (1, 0))
            parallel = hdir if horiz else vdir
            rewind, forward = (self._probe(x, y, dir, virtual)
                               for dir in parallel)
            return rewind[::-1] + forward[1:]

    def get_crossword(self, word, vec, pos):
        virtual = deepcopy(self)
        if virtual.place(word, vec):
            x, y, horiz = pos
            hdir = ((0, -1), (0, 1))
            vdir = ((-1, 0), (1, 0))
            perpendi = vdir if horiz else hdir
            rewind, forward = (self._probe(x, y, dir, virtual)
                               for dir in perpendi)
            return rewind[::-1] + forward[1:]

    def validate_vicinity(self, word, vec):
        valid = False
        x, y, horiz = vec
        for i in range(len(word)):
            cx, cy = (x, y + i) if horiz else (x + i, y)
            pos = (cx, cy, horiz)
            crossword = self.get_crossword(word, vec, pos, self)
            if crossword and len(crossword) > 1:
                valid = True
                if not self._valid(crossword):
                    return False
        if self.is_empty():
            mx, my = self.get_center()
            valid_range = my - y if horiz else mx - x
            if valid_range in range(len(word)):
                if horiz:
                    if x == mx:
                        valid = True
                else:
                    if y == my:
                        valid = True
        return valid

    def validate(self, tiles, word, vec):
        x, y, horiz = vec
        # we need at least a free case to put a tile in
        # for instance : word=radar / board=radar / tiles=aadrr
        # is not a valid move
        free = False
        remaining = list(tiles)
        for i, letter in enumerate(word):
            tx, ty = (x, y + i) if horiz else (x + i, y)
            if (tx, ty) not in self.coords():
                return False
            if not self.is_free(tx, ty):
                if letter != self.get_letter(tx, ty):
                    return False
            else:
                free = True
                if letter not in remaining:
                    if '*' in remaining:
                        remaining.remove('*')
                    else:
                        return False
                else:
                    remaining.remove(letter)
        return free

    def _get_chunks(self, mask):
        for chunk in mask.split('_'):
            if chunk:
                yield chunk

    def get_line_mask(self, x, y, horiz):
        if horiz:
            yield self._warp_probe(x, 0, (0, 1))
        else:
            yield self._warp_probe(0, y, (1, 0))

    def _warp_probe(self, x, y, dir):
        if (x, y) not in self.coords():
            return ''
        else:
            dx, dy = dir
            return self.get_letter(x, y)
            + self._warp_probe(x + dx, y + dy, dir)

    def _probe(self, x, y, dir):
        if (x, y) not in self.coords() or self.is_free(x, y):
            return ''
        else:
            dx, dy = dir
            return self.get_letter(x, y)
            + self._probe(x + dx, y + dy, dir)
