"""
    Exercice du code de Vigenère
    MOOC Python -- Semaine 4
    Auteur : Sébastien Hoarau
    Date : 2018-10-10
"""

from string import ascii_letters
from itertools import cycle


class Code:

    def __init__(self, cle):
        self.alpha = ascii_letters
        self.size = len(self.alpha)
        self.infinite_key = cycle(cle)

    def translate_one_car(self, x, mode):
        """ Donne le caractère codant/decodant x en utilisant la 
            formule suivante (indice sont les indices des caractères
            dans self.alpha, l'alphabet utilisé) :
            indice_new_car = (indice_x + indice_k) % self.size
            k étant la lettre de la clé obtenue de façon cyclique """
        if x in self.alpha:
            k = next(self.infinite_key)
            i = self.alpha.index(x)
            j = mode * self.alpha.index(k)
            return self.alpha[(i + j) % self.size]
        else:
            return x


    def translate(self, msg, mode=1):
        """ Effectue la translation positive (mode = 1) pour le codage
            ou négative (mode = -1) pour le décodage sur chacun des caractères
            du message (initial ou codé) """
        return ''.join([self.translate_one_car(c, mode) for c in msg])


    def encode(self, msg):
        return self.translate(msg)

    def decode(self, coded):
        return self.translate(coded, -1)


def main():
    cle = 'musique'
    msg = "J'adore ecouter FUN-RADIO toute la journee"
    codec = Code(cle)
    coded = codec.encode(msg)
    print('Message codé :')
    print(coded)
    print('Message original :')
    print(codec.decode(coded))


if __name__ == '__main__':
    main()




