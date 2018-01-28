# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 18:08:54 2018

@author: francois.sidoroff
"""

import mastermind as mm

with open("mastermind.jnl", "w", encoding='utf-8')as journal:
    jeu = mm.Mastermind(journal, 'ABCDEF', 4)
    jeu.partie(0, 1)
