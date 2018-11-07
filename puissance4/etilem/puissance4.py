#!/usr/bin/env python3
# coding: utf-8
# pylint: disable=c0103,r0903
"""
Programme principal du jeu Puissance4
"""

from lib import Human, AI, Simu

Simu(Human(), AI(), "fr").start()
