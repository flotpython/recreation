
from re import search
from .solver import Solver


class Simu():

    def start(self):

        solver = Solver()

        try:
            choice = str(input("Vos lettres : ")).upper().strip()
            if search("[^a-zA-Z*]", choice) or search("\\*{3,}", choice):
                raise ValueError
        except ValueError:
            choice = ""

        anagrams = set(solver.find_anagrams(choice))
        if anagrams:
            print(anagrams)
            print("J'ai trouvé", len(anagrams), "anagrammes !")
