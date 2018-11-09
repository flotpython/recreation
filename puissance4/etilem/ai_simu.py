#!/usr/bin/env python3
# coding: utf-8
"""
simulation de partie IA contre IA
"""

from lib import AI, Simu, LENGTH

Simu(AI(), AI(), "fr").start()

print(f"\nLongueur du segment recherché : {LENGTH}")
