#!/usr/bin/env python3
# coding: utf-8

# je configure pytlint pour qu'il ignore l'absence de docstrings
# pylint: disable=c0111

import random

class Myst:
    """
    Devinez le nombre mytérieux... par recherche dichotomique bien sûr !
    Jeu disponible, au choix, en français ou en anglais !
    """

    def __init__(self, minimum, maximum, locale):

        self.locales = ('fr', 'en') # localisations dispos (cf put_on_screen)

        # on vérifie les paramètres minimum, maximum et locale
        if (isinstance(minimum, int)
                and isinstance(maximum, int)
                and minimum >= 0
                and maximum > minimum
                and locale in self.locales):
            self.min, self.max = (minimum, maximum)
            self.myst = random.randint(self.min, self.max)
            self.locale = locale
        else:
            print(f"Conditions initiales incorrectes : "
                 f"vérifiez les bornes ({minimum} .. {maximum}) "
                 f"ou la locale utilisée ({locale}).")
            exit(1)

        self.count = 0 # compteur de tentatives
        self.chall = -1 # nombre proposé par le challenger

        # dictionnaire profondeur 2 des phrases à afficher
        # suivant la localisation
        self.put_on_screen = {
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

    def feedback(self, key, *params):
        return self.put_on_screen[key][self.locale].format(*params)

    def is_myst_number(self):

        # demande à l'utilisateur un nombre compris entre 2 bornes
        try:
            self.chall = int(input(self.feedback('choice', self.min, self.max)))
        # attrape l'exception en cas de valeur impropre
        except ValueError:
            print(self.feedback('invalid_input'))
            return False
        # incrémente le nombre de tentatives quelque soit l'entrée fournie
        finally:
            self.count += 1
        # différents tests de comparaison entre le nombre fourni
        # et le nombre mystère
        if self.chall > self.max:
            print(self.feedback('too_big_out_of_range', self.chall, self.max))
        elif self.chall < self.min:
            print(self.feedback('too_small_out_of_range', self.chall, self.min))
        elif self.chall > self.myst:
            print(self.feedback('too_big', self.chall))
        elif self.chall < self.myst:
            print(self.feedback('too_small', self.chall))
        else:
            print(self.feedback('jackpot', self.myst, self.count))
        return self.chall == self.myst

    def start(self):
        # on boucle tant que le nombre mystère n'est pas découvert
        while not self.is_myst_number():
            pass

# TODO: utiliser argparse pour que l'utilisateur puisse choisir sa langue
#       avec une option sur la ligne de commande

myst = Myst(0, 1000, 'fr')
myst.start()
