"""
    Exercice du code de Vigenère
    MOOC Python -- Semaine 4
    Auteur : Sébastien Hoarau
    Date : 2018-10-10
"""
from string import ascii_letters

class Code:

    def __init__(self, cle):
        self.alpha = ascii_letters
        self.size = len(self.alpha)
        self.cle = cle
        self.pass_phrase = ''

    def set_pass_phrase(self, msg):
        i = 0
        for c in msg.lower():
            if c in self.alpha:
                self.pass_phrase += self.cle[i]
                i = (i + 1) % len(self.cle)
            else:
                self.pass_phrase += ' '


    def translate(self, msg, mode=1):
        """ Effectue la translation positive (mode = 1) pour le codage
            ou négative (mode = -1) pour le décodage """
        self.set_pass_phrase(msg)
        coded_or_decoded = ''
        for idc, c in enumerate(msg):
            if c in self.alpha:
                i = self.alpha.index(c)
                j = mode * self.alpha.index(self.pass_phrase[idc])
                coded_or_decoded +=  self.alpha[(i + j) % self.size]
            else:
                coded_or_decoded += c
        return coded_or_decoded


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




