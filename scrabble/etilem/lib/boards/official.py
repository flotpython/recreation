"""
Official Scrabble board
"""
from .common import Common


class Board(Common):

    TYPE = "official"
    RANGE = 15
    RG = 0  # regular spot
    ST = 1  # start spot
    LD = 2  # letter's double bonus
    LT = 3  # letter's triple bonus
    WD = 4  # word's double bonus
    WT = 5  # word's triple bonus

    bonus = (  # TODO: should use symetries to reduce structure by quarter
        (WT, RG, RG, LD, RG, RG, RG, WT, RG, RG, RG, LD, RG, RG, WT),
        (RG, WD, RG, RG, RG, LT, RG, RG, RG, LT, RG, RG, RG, WD, RG),
        (RG, RG, WD, RG, RG, RG, LD, RG, LD, RG, RG, RG, WD, RG, RG),
        (LD, RG, RG, WD, RG, RG, RG, LD, RG, RG, RG, WD, RG, RG, LD),
        (RG, RG, RG, RG, WD, RG, RG, RG, RG, RG, WD, RG, RG, RG, RG),
        (RG, LT, RG, RG, RG, LT, RG, RG, RG, LT, RG, RG, RG, LT, RG),
        (RG, RG, LD, RG, RG, RG, LD, RG, LD, RG, RG, RG, LD, RG, RG),
        (WT, RG, RG, LD, RG, RG, RG, ST, RG, RG, RG, LD, RG, RG, WT),
        (RG, RG, LD, RG, RG, RG, LD, RG, LD, RG, RG, RG, LD, RG, RG),
        (RG, LT, RG, RG, RG, LT, RG, RG, RG, LT, RG, RG, RG, LT, RG),
        (RG, RG, RG, RG, WD, RG, RG, RG, RG, RG, WD, RG, RG, RG, RG),
        (LD, RG, RG, WD, RG, RG, RG, LD, RG, RG, RG, WD, RG, RG, LD),
        (RG, RG, WD, RG, RG, RG, LD, RG, LD, RG, RG, RG, WD, RG, RG),
        (RG, WD, RG, RG, RG, LT, RG, RG, RG, LT, RG, RG, RG, WD, RG),
        (WT, RG, RG, LD, RG, RG, RG, WT, RG, RG, RG, LD, RG, RG, WT),
    )
