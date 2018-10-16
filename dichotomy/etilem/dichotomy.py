
# coding: utf-8

import random

class Myst:

    """ Devinez le nombre mytérieux...
            par recherche dichotomique bien sûr !
        Jeu disponible, au choix, en français ou en anglais !
    """

    def __init__(self, minimum, maximum, locale):

        # on vérifie les paramètres minimum, maximum et locale
        if isinstance(minimum, int) \
        and isinstance(maximum, int) \
        and minimum >= 0 \
        and maximum > minimum \
        and locale in ('fr', 'en'):
            self.min, self.max = (minimum, maximum)
            self.myst = random.randint(self.min, self.max)
            self.locale = locale
        else:
            exit(f"Conditions initiales incorrectes : vérifiez les bornes minimale ({minimum}) et maximale ({maximum}) ou la locale utilisée ({locale}).")

        self.count = 0 # compteur de tentatives
        self.chall = -1 # nombre proposé par le challenger

        # dictionnaire profondeur 2 des phrases à afficher suivant la localisation
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

    def isMystNumber(self):

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
            # différents test de comparaison du nombre fourni avec le nombre mystère
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
        while not self.isMystNumber():
            pass

myst = Myst(0, 1000, 'fr').start()
