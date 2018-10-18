#!/usr/bin/env python3
# coding: utf-8

# je configure pytlint pour qu'il ignore l'absence de docstrings
# pylint: disable=c0111

import argparse
import random

class Phrases:
    """
    Différentes phrases utilisées pour interagir avec le joueur
    """
    def __init__(self):
        self.available_locales = ('fr', 'en')
        self.phrases = {
            'choice': {
                'fr': "Choisissez un nombre entre {} et {} : ",
                'en': "Choose a number between {} and {} : ",
            },
            'invalid_input': {
                'fr': "Ce n'est pas un entier positif.",
                'en': "This is not a positive integer.",
            },
            'too_big_out_of_range': {
                'fr': "{} doit être inférieur à {}.",
                'en': "{} must be lesser than {}.",
            },
            'too_small_out_of_range': {
                'fr': "{} doit être supérieur à {}.",
                'en': "{} must be greater than {}.",
            },
            'too_big': {
                'fr': "{} est trop grand !",
                'en': "{} is too big !",
            },
            'too_small': {
                'fr': "{} est trop petit !",
                'en': "{} is too small !",
            },
            'jackpot': {
                'fr': "Bravo, vous avez trouvé {} en {} coups !",
                'en': "Bravo, you've just found {} in {} tries !",
            },
        }
    def get(self, key, locale, *params):
        return self.phrases[key][locale].format(*params)

class Myst:
    """
    Devinez le nombre mytérieux... par recherche dichotomique bien sûr !
    """
    def __init__(self, minimum, maximum, locale):

        self.dialog = Phrases()

        # on vérifie les paramètres minimum, maximum et locale
        if not isinstance(minimum, int):
            raise ValueError(f"minimum ({minimum}) doit être un entier.")
        if not isinstance(maximum, int):
            raise ValueError(f"maximum ({maximum}) doit être un entier.")
        if minimum < 0:
            raise ValueError(f"minimum ({minimum}) doit être positif ou nul.")
        if maximum <= minimum:
            raise ValueError(f"maximum ({maximum}) doit être supérieur à {minimum}")
        if locale not in self.dialog.available_locales:
            raise ValueError(f"locale inconnue ({locale}), "
                             f"choisissez-la parmi {self.dialog.available_locales}")

        self.min, self.max = (minimum, maximum)
        self.myst = random.randint(self.min, self.max)
        self.locale = locale

        self.count = 0 # compteur de tentatives

    def feedback(self, key, *params):
        return self.dialog.get(key, self.locale, *params)

    def ask_for_number(self):
        """
        demande à l'utilisateur un nombre compris entre 2 bornes
        """
        try:
            chall = int(input(self.feedback('choice', self.min, self.max)))
        # attrape l'exception en cas de valeur impropre
        except ValueError:
            print(self.feedback('invalid_input'))
            return False
        # incrémente le nombre de tentatives quelque soit l'entrée fournie
        finally:
            self.count += 1
        return chall

    def is_myst_number(self, chall):
        """
        différents tests de comparaison entre le nombre fourni et le nombre mystère
        """
        if chall is False: # cas 'invalid_input' dans ask_for_number()
            return False
        if chall > self.max:
            print(self.feedback('too_big_out_of_range', chall, self.max))
        elif chall < self.min:
            print(self.feedback('too_small_out_of_range', chall, self.min))
        elif chall > self.myst:
            print(self.feedback('too_big', chall))
        elif chall < self.myst:
            print(self.feedback('too_small', chall))
        else:
            print(self.feedback('jackpot', self.myst, self.count))
        return chall == self.myst

    def start(self):
        # on boucle tant que le nombre mystère n'est pas découvert
        while not self.is_myst_number(self.ask_for_number()):
            pass

# utilise argparse pour que l'utilisateur puisse choisir sa langue
# avec une option sur la ligne de commande
parser = argparse.ArgumentParser()
parser.add_argument("-l", "--locale", default='fr', help="choix de la langue parmi 'fr' et 'en'")
args = parser.parse_args()

Myst(0, 1000, args.locale).start()
