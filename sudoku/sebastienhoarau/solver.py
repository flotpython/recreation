#!/usr/bin/env python3

""" 
SOLVEUR DE SUDOKUS 

Principe : Les grilles de sudoku sont représentées par un fichier 
stockant pour chaque grille un identifiant et des données sur une 
ligne (une chaine de 81 caractères), identifiant et donnée sont 
séparés par un espace

Le solveur prend un tel fichier ainsi qu'un fichier contenant des 
identifiants et va résoudre toutes les grilles correspondantes puis
afficher un résumé avec notamment le nombre de grilles résolues sans
et avec backtrack ainsi que le temps moyen.

Le but ici est de faire tourner ce solveur sur un fichier contenant 
49151 grilles de 17 cases initiales (sudoku17) et d'essayer de toutes 
les résoudres *sans* backtrack.

Synopsis

./solver.py [-a global_file] [-f filter_file] [grid_id]

-a global_file  Utilise le fichier global_file comme fichier de grilles
                de sudoku. Ce fichier doit être rangé au même niveau 
                dans un dossier Grilles.
                Par défaut global_file vaut sudoku17

-f filter_file  Utilise le fichier filter_file contenant des noms de
                grilles pour ne résoudre que celles là. Ce fichier
                doit être rangé au même niveau dans un dossier Filtres.
                Si aucun fichier de filtre n'est fourni alors toutes les
                grilles du fichier global seront résolues.

grid_id         Un nom de grille censé être présent dans le fichier global.
                Pour résoudre une grille unique.



Auteur : Sébastien Hoarau
Date   : 2018.10.29
"""

REP_GRID = 'Grilles'
REP_FILTER = 'Filtres'
DEFAULT_SUDOKUS = 'sudoku17'
DEFAULT_FILTER = 'avec_backtrack'
SUDOKU17_SIZE = 49151 

import pathlib
import argparse
import random
import solve_sudoku as sos

class Solver:

    def __init__(self):
        self.main_filename = ''         # nom du fichier principal contenant toutes les grilles
        self.snd_filename = ''          # le fichier secondaire avec les identifiants des grilles à résoudre
        self.datas = {}                 # dictionnaire stockant les données de toutes les grilles
        self.sudokus_to_solve = set()   # l'ensemble des identifiants à résoudre
        self.sudokus = []               # la liste des sudokus créés et résolus
        self.verbose = True             # pour afficher les détails
        self.techniques = {tech:0 for tech in sos.TECHNIQUES}
    


    def settings(self):
        """
        Pour récupérer les fichiers nécessaires, régler le solveur
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('id_file', nargs='?', help='A sudoku id, teh sudoku to solve')
        parser.add_argument('-a', '--all', help='The file name of all sudokus.')
        parser.add_argument('-f', '--filter', help='The file name of sudokus id we want to solve.')
        parser.add_argument('-v', '--verbose', help='Print details for each sudoku.',
                                action='store_true')
        args = parser.parse_args()

        # le fichier contenant toutes les grilles
        #
        if args.all:
            main_filename = pathlib.Path.cwd() / REP_GRID / args.all
        else:
            main_filename = pathlib.Path.cwd() / REP_GRID / DEFAULT_SUDOKUS

        # si on a 1 seul  identifiant de fichier c'est lui qu'on va résoudre
        if args.id_file:
            filtername = pathlib.Path.cwd() / REP_FILTER / 'default_filter'
            with open(filtername, 'w') as output:
                output.write(f'{args.id_file}\n')
        # sinon on regarde dans le fichier filtre
        elif args.filter:
            filtername = pathlib.Path.cwd() / REP_FILTER / args.filter
        # sinon pas de filtre et on prendra tous les fichiers
        else:
            filtername = ''

        with open(main_filename, 'r') as all_sudokus:
            for index, one_sudoku in enumerate(all_sudokus):
                infos = one_sudoku.split()
                if len(infos) == 2:
                    id_sudoku, data_sudoku = infos
                else:
                    id_sudoku, data_sudoku = index, infos[0]
                self.datas[id_sudoku] = data_sudoku

        if filtername:
            with open(filtername, 'r') as some_sudokus:
                for id_sudoku in some_sudokus:
                    self.sudokus_to_solve.add(id_sudoku[:-1])
        else:
            self.sudokus_to_solve = set(self.datas.keys())

        self.verbose = args.verbose or len(self.sudokus_to_solve) <= 5



    def start(self):
        for index, id_sudoku in enumerate(self.sudokus_to_solve):
            if not self.verbose:
                print(f'{index:05} : {id_sudoku}')
            current_sudoku = sos.Sudoku(id_sudoku, self.datas[id_sudoku])
            if self.verbose:
                print(current_sudoku)
            current_sudoku.solve()
            if self.verbose:
              current_sudoku.analyse()
            self.sudokus.append(current_sudoku)


    def end(self):
        """
        Terminer le solveur c'est afficher un résumé des grilles résolues
        résumé du nombre de grilles résolues avec backtrack et sans.
        """
        counts = [0, 0]
        tps = [0, 0]
        nbgrilles = len(self.sudokus)
        nbcar = len(f'{nbgrilles}')
        for current_sudoku in self.sudokus:
            if self.verbose:
                print(current_sudoku)
            nb_backtrack = current_sudoku.techniques['backtracking']
            crt_tps = current_sudoku.temps
            name = current_sudoku.id
            avec_backtrack = nb_backtrack > 0 
            counts[avec_backtrack] += 1
            tps[avec_backtrack] += crt_tps
            for tech in self.techniques:
                self.techniques[tech] += int(current_sudoku.techniques[tech] > 0)
        for i in range(2):
            try:
                tps[i] = tps[i] / counts[i]
            except:
                pass
        abstract = f'\nRésumé des {nbgrilles} grilles :\n'\
            f'* Avec backtrack : {counts[1]:{nbcar}} ({counts[1]/nbgrilles:>.1%}), '\
            f'temps moyen {tps[1]:.3f}s\n'\
            f'* Sans backtrack : {counts[0]:{nbcar}} ({counts[0]/nbgrilles:>.1%}), '\
            f'temps moyen {tps[0]:.3f}s\n'
        nbcar2 = max(len(s) for s in sos.TECHNIQUES)
        abstract += f'Les techniques utilisées :\n'
        for tech in sos.TECHNIQUES:
            nbtech = self.techniques[tech]
            abstract += f'* {tech:{nbcar2}} : {nbtech:{nbcar}} utilisations ({nbtech/nbgrilles:>.1%})\n'
        print(abstract)




# -- MAIN -- 

my_solver = Solver()
my_solver.settings()
my_solver.start()
my_solver.end()



