# coding: utf-8
"""
module d'interactions homme <-> machine
"""

class Phrases:
    """
    Différentes phrases utilisées pour interagir avec le joueur
    """
    def __init__(self, locale):
        self.available_locales = ('fr', 'en')
        self.locale = locale
        self.phrases = {
            'choice': {
                'fr': "Dans quelle colonne jouez-vous ? : ",
                'en': "Which column do you play ? : ",
            },
            'invalid': {
                'fr': "Ce n'est pas un nombre.",
                'en': "This is not a number",
            },
            'has_played': {
                'fr': "{}  a joué {}",
                'en': "{}  has played {}",
            },
            'has_won': {
                'fr': "et gagne !",
                'en': "and win !",
            },
            'deuce': {
                'fr': "Égalité !",
                'en': "Deuce !",
            },
        }

    def __call__(self, key, *params):
        """
        Renvoit une phrase suivant la clé demandée
        """
        return self.phrases[key][self.locale].format(*params)
