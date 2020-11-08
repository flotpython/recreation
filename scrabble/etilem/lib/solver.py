
from itertools import combinations
from .dicts import Dict
from copy import deepcopy
import multiprocessing

class Solver():

    dict = Dict()

    def find_anagrams(self, word, chunks=[]):
        data = self._pack(word)
        for i in range(word.count('*')):
            data = self._unpack(data)
        for key in data:
            for i in range(len(key) + len(''.join(chunks))):
                for hash in combinations(list(key) + chunks, i + 2):
                    hash = self._word_to_key(''.join(hash))
                    for origin in self.dict.words.get(''.join(hash), []):
                        yield origin

    def find_playable_words(self, tiles, board):
        for num in board.diagonal():
            for mask, horiz in self._get_line_masks(num, board):
                for anagram in self.find_anagrams(tiles, list(self._get_chunks(mask))):
                    with multiprocessing.Pool():
                        for x, y in self._get_line_anchors(num, horiz, board):
                            vec = (x, y, horiz)
                            full_word = self.get_evenword(anagram, vec, board)
                            if self._valid(full_word):
                                vec = self._get_new_vec(full_word, anagram, vec)
                                if board.validate(tiles, full_word, vec):
                                    if self._validate_vicinity(full_word, vec, board):
                                        yield full_word, vec

    def get_evenword(self, word, vec, board):
        virtual = deepcopy(board)
        if virtual.place(word, vec):
            x, y, horiz = vec
            hdir = ((0, -1), (0, 1))
            vdir = ((-1, 0), (1, 0))
            parallel = hdir if horiz else vdir
            rewind, forward = (self._probe(x, y, dir, virtual)
                               for dir in parallel)
            return rewind[::-1] + forward[1:]

    def get_crossword(self, word, vec, pos, board):
        virtual = deepcopy(board)
        if virtual.place(word, vec):
            x, y, horiz = pos
            hdir = ((0, -1), (0, 1))
            vdir = ((-1, 0), (1, 0))
            perpendi = vdir if horiz else hdir
            rewind, forward = (self._probe(x, y, dir, virtual)
                               for dir in perpendi)
            return rewind[::-1] + forward[1:]

    def _validate_vicinity(self, word, vec, board):
        valid = False
        x, y, horiz = vec
        for i in range(len(word)):
            cx, cy = (x, y + i) if horiz else (x + i, y)
            pos = (cx, cy, horiz)
            crossword = self.get_crossword(word, vec, pos, board)
            if crossword and len(crossword) > 1:
                valid = True
                if not self._valid(crossword):
                    return False
        if board.is_empty():
            mx, my = board.get_center()
            valid_range = my - y if horiz else mx - x
            if valid_range in range(len(word)):
                if horiz:
                    if x == mx:
                        valid = True
                else:
                    if y == my:
                        valid = True
        return valid

    def _get_line_anchors(self, num, horiz, board):
        for i in range(board.RANGE):
            x, y = (num, i) if horiz else (i, num)
            px, py = (num, i - 1) if horiz else (i - 1, num)
            nx, ny = (num, i + 1) if horiz else (i + 1, num)
            if not board.is_free(x, y):
                yield x, y
            else:
                if (px, py) in board.coords() and not board.is_free(px, py):
                    yield x, y
                if (nx, ny) in board.coords() and not board.is_free(nx, ny):
                    yield x, y
                if board.is_empty():
                    cx, cy = board.get_center()
                    if x == cx or y == cy:
                        yield x, y

    def _get_new_vec(self, full_word, word, vec):
        x, y, horiz = vec
        i = full_word.find(word)
        if i == 0:
            return vec
        else:
            new = (x - i, y, True) if horiz else (x, y - i, False)
            return new

    def _get_chunks(self, mask):
        for chunk in mask.split('_'):
            if chunk:
                yield chunk

    def _get_line_masks(self, num, board):
        h_line = self._warp_probe(num, 0, (0, 1), board)
        v_line = self._warp_probe(0, num, (1, 0), board)
        yield h_line, True
        yield v_line, False

    def _probe(self, x, y, dir, board):
        if (x, y) not in board.coords() or board.is_free(x, y):
            return ''
        else:
            dx, dy = dir
            return board.get_letter(x, y) + self._probe(x + dx, y + dy, dir, board)

    def _warp_probe(self, x, y, dir, board):
        if (x, y) not in board.coords():
            return ''
        else:
            dx, dy = dir
            return board.get_letter(x, y) + self._warp_probe(x + dx, y + dy, dir, board)

    def _valid(self, word):
        key = self._word_to_key(word)
        return word in self.dict.words.get(key, [])

    def _word_to_key(self, word):
        if word:
            return ''.join(sorted(word.upper()))
        else:
            return ''

    def _expand(self, word=''):
        alphabet = (chr(65 + i) for i in range(26))
        for car in alphabet:
            yield word + car

    def _pack(self, word):
        if '*' in word:  # word = "fo*o*"
            key = self._word_to_key(word)  # key = "**FOO"
            for exp in self._expand(key[1:]): # exp = *FOOA, *FOOB, ... , *FOOZ
                yield self._pack(exp)
        else:
            yield self._word_to_key(word)

    def _unpack(self, data):
        for gen in data:
            for i in gen:
                yield i
