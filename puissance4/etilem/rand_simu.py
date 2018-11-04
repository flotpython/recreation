#!/usr/bin/env python3
# coding: utf-8
# pylint: disable=c0103,r0903
"""
simulation aléatoire de partie
"""

from lib import Random, Simu

length = 5

Simu(Random(), Random(), "fr", length=length).start()

print(f"\nLongueur du segment recherché : {length}")
