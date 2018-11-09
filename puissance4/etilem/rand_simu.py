#!/usr/bin/env python3
# coding: utf-8
"""
simulation aléatoire de partie
"""

from lib import Random, Simu, LENGTH

Simu(Random(), Random(), "fr").start()

print(f"\nLongueur du segment recherché : {LENGTH}")
