# Analyse des 49151 grilles de sudoku


## 2018.10.26

* Nettoyage du code : identificateurs  harmonisés en anglais pour les variables en tout cas.
* Optimisation du calcul des pair cachées, triple cachés ainsi que la recherche des singletons.
* Création de deux fichiers avec les noms des grilles : 
	1. avec_backtrack contient les noms des 22833 grilles nécessitant encore du backtracking
	2. sans_backtrack contient les 26318 autres

Dernières stats effectuées (rangées dans le dossier Stats) :

* Sans backtrack : 26318 grilles, temps moyen : 0.007s
* Avec backtrack : 22833 grilles, temps moyen : 0.034s


## 2018.10.28

* Ajout recherche locked type 1. A permis à qq grilles de passer sans backtrack

Dernières stats effectuées (rangées dans le dossier Stats) :

* Sans backtrack : 37381 grilles, temps moyen : 0.008s
* Avec backtrack : 11770 grilles, temps moyen : 0.017s


## 2018.10.29

* Refonte du squelette : 
	- classe_sudoku.py -> sudoku.py refonte de l'initialisation d'un sudoku. On crée avec une donnée de type chaine de 81 caractères 
	- sudoku.py -> solver.py ce dernier a été simplifié. On utilise argparse pour passer qq options en revue


## 2018.10.30

* Ajout recherche des naked subsets

Dernières stats effectuées :

* Sans backtrack : 38742 grilles, temps moyen : 0.008s
* Avec backtrack : 10409 grilles, temps moyen : 0.022s

## 2018.11.05

* Refonte avec introduction des maisons et 3 modules .py :
	- solver.py qui gère de récupérer les grilles à résoudre et lance l'affaire
	- solve_sudoku.py qui met en place les stratégies de résolution
	- struct_sudoku.py qui code la structure d'un sudoku avec les notions de sudoku (ensemble de cellules en gros), les cellules et les maisons (regroupement logiques de cellules)
* Du travail de cohérence reste à faire
* Mise en oeuvre des techniques xy-wing et basic-fish

Dernières stats effectuées :

* Sans backtrack : 48636 (99.0%), temps moyen 0.023s
* Avec backtrack :   515 (1.0%), temps moyen 0.

* naked_single   : 49077 utilisations (99.8%)
* hidden_single  : 49151 utilisations (100.0%)
* intersections  : 24670 utilisations (50.2%)
* hidden_subsets : 14428 utilisations (29.4%)
* naked_subsets  :  2884 utilisations (5.9%)
* basic_fish     : 10213 utilisations (20.8%)
* xy-wing        :   191 utilisations (0.4%)

## 2018.11.06

* Correction bugs dans basic-fish (qui explique les stats fausses)
* Introduction de w-wing

Dernières stats effectuées :

* Sans backtrack : 42796 (87.1%), temps moyen 0.021s
* Avec backtrack :  6355 (12.9%), temps moyen 0.112s

naked_single   : 46916 utilisations (95.5%)
hidden_single  : 49147 utilisations (100.0%)
intersections  : 24441 utilisations (49.7%)
hidden_subsets : 13938 utilisations (28.4%)
naked_subsets  :  2125 utilisations (4.3%)
basic_fish     :  9938 utilisations (20.2%)
xy-wing        :  1674 utilisations (3.4%)
w-wing         :  2608 utilisations (5.3%)

