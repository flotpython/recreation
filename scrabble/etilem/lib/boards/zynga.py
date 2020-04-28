"""
Zynga version of Scrabble used on Facebook (Words with Friends)
"""
from .common import Common


class Board(Common):

    TYPE = "zynga"
    RANGE = 11
    RG = 0  # regular spot
    ST = 1  # start spot
    LD = 2  # letter's double bonus
    LT = 3  # letter's triple bonus
    WD = 4  # word's double bonus
    WT = 5  # word's triple bonus

    bonus = (  # TODO: should use symetries to reduce structure by quarter
        (LT, RG, WT, RG, RG, RG, RG, RG, WT, RG, LT),
        (RG, WD, RG, RG, RG, WD, RG, RG, RG, WD, RG),
        (WT, RG, LT, RG, LD, RG, LD, RG, LT, RG, WT),
        (RG, RG, RG, LT, RG, RG, RG, LT, RG, RG, RG),
        (RG, RG, LD, RG, RG, RG, RG, RG, LD, RG, RG),
        (RG, WD, RG, RG, RG, ST, RG, RG, RG, WD, RG),
        (RG, RG, LD, RG, RG, RG, RG, RG, LD, RG, RG),
        (RG, RG, RG, LT, RG, RG, RG, LT, RG, RG, RG),
        (WT, RG, LT, RG, LD, RG, LD, RG, LT, RG, WT),
        (RG, WD, RG, RG, RG, WD, RG, RG, RG, WD, RG),
        (LT, RG, WT, RG, RG, RG, RG, RG, WT, RG, LT),
    )
