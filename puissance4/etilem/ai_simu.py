#!/usr/bin/env python3
# coding: utf-8
# pylint: disable=c0103,r0903
"""
simulation aléatoire de partie
"""

from lib import AI, Simu, LENGTH

Simu(AI(), AI(), "fr", length=LENGTH).start()

print(f"\nLongueur du segment recherché : {LENGTH}")
