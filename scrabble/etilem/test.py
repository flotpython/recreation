
import unittest
from lib import Dict
from lib import Board
from lib import Solver


class TestSolver(unittest.TestCase):

    def setUp(self):
        self.obj = Solver()

    def test_find_anagrams(self):
        word = "VEILL"
        self.assertIn("REVEILLEZ", self.obj.find_anagrams(word, ['RE', 'EZ']))
        tiles = "AE"
        word = "RASER"
        self.assertIn(word, self.obj.find_anagrams(tiles, ['R', 'S', 'R']))
        tiles = "ARE"
        word = "RARE"
        self.assertIn(word, self.obj.find_anagrams(tiles, ['R']))


class TestDict(unittest.TestCase):

    def setUp(self):
        self.obj = Dict()

    def test_is_not_empty(self):
        self.assertTrue(len(self.obj.words) > 0)

    def test_word_is_in(self):
        word = "EMNOY"
        self.assertIn(word, self.obj.words)

    def test_word_is_not_in(self):
        word = "MOYEN"
        self.assertNotIn(word, self.obj.words)


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.obj = Board()
        if self.obj.TYPE == "official":
            self.st_map = ((7, 7),)
            self.ld_map = ((0, 3), (0, 11),
                           (2, 6), (2, 8),
                           (3, 0), (3, 7), (3, 14),
                           (6, 2), (6, 6), (6, 8), (6, 12),
                           (7, 3), (7, 11),
                           (8, 2), (8, 6), (8, 8), (8, 12),
                           (11, 0), (11, 7), (11, 14),
                           (12, 6), (12, 8),
                           (14, 3), (14, 11))
            self.lt_map = ((1, 5), (1, 9),
                           (5, 1), (5, 5), (5, 9), (5, 13),
                           (9, 1), (9, 5), (9, 9), (9, 13),
                           (13, 5), (13, 9))
            self.wd_map = ((1, 1), (2, 2), (3, 3), (4, 4),
                           (10, 10), (11, 11), (12, 12), (13, 13),
                           (1, 13), (2, 12), (3, 11), (4, 10),
                           (10, 4), (11, 3), (12, 2), (13, 1),
                           (1, 13), (2, 12), (3, 11), (4, 10))
            self.wt_map = ((0, 0), (0, 7), (0, 14),
                           (7, 0), (7, 14),
                           (14, 0), (14, 7), (14, 14))
        elif self.obj.TYPE == "zynga":
            self.st_map = ((5, 5),)
            self.ld_map = ((2, 4), (2, 6),
                           (4, 2), (4, 8),
                           (6, 2), (6, 8),
                           (8, 4), (8, 6))
            self.lt_map = ((0, 0), (0, 10),
                           (2, 2), (2, 8),
                           (3, 3), (3, 7),
                           (7, 3), (7, 7),
                           (8, 2), (8, 8),
                           (10, 0), (10, 10))
            self.wd_map = ((1, 1), (1, 5), (1, 9),
                           (5, 1), (5, 9),
                           (9, 1), (9, 5), (9, 9))
            self.wt_map = ((0, 2), (0, 8),
                           (2, 0), (2, 10),
                           (8, 0), (8, 10),
                           (10, 2), (10, 8))

    def test_wt_bonus_is_in_matrix(self):
        for x, y in self.wt_map:
            self.assertEqual(self.obj.bonus[x][y], self.obj.WT)

    def test_wd_bonus_is_in_matrix(self):
        for x, y in self.wd_map:
            self.assertEqual(self.obj.bonus[x][y], self.obj.WD)

    def test_lt_bonus_is_in_matrix(self):
        for x, y in self.lt_map:
            self.assertEqual(self.obj.bonus[x][y], self.obj.LT)

    def test_ld_bonus_is_in_matrix(self):
        for x, y in self.ld_map:
            self.assertEqual(self.obj.bonus[x][y], self.obj.LD)

    def test_st_bonus_is_in_matrix(self):
        for x, y in self.st_map:
            self.assertEqual(self.obj.bonus[x][y], self.obj.ST)

    def test_rg_bonus_is_in_matrix(self):
        for x in range(self.obj.RANGE):
            for y in range(self.obj.RANGE):
                if (x, y) in self.st_map:
                    continue
                elif (x, y) in self.ld_map:
                    continue
                elif (x, y) in self.lt_map:
                    continue
                elif (x, y) in self.wd_map:
                    continue
                elif (x, y) in self.wt_map:
                    continue
                self.assertEqual(self.obj.bonus[x][y], self.obj.RG)

    def test_is_not_empty(self):
        self.assertTrue(len(self.obj.letter_score) > 0)

    def test_letter_is_in(self):
        letter = "*"
        self.assertIn(letter, self.obj.letter_score)

    def test_letter_is_not_in(self):
        letter = "À"
        self.assertNotIn(letter, self.obj.letter_score)


if __name__ == '__main__':
    unittest.main()
