# Sudoku

Manipuler des objets, des références, de la récursivité...
Le sudoku a été pas mal étudié et offre de nombreuses possibilités de codage. Un ami m'a proposé un fichier contenant 49151 grilles de sudoku avec 17 cases remplies (le minimum je crois pour garantir une unique solution)

Un semblant de cahier des charges :

## Description :

Tout le monde connait le sudoku : une grille 9x9 que l'on doit remplir avec les entiers de 1 à 9, en respectant la contrainte du *all_diff* sur chacune des lignes, chacune des colonnes et chacun des mini carré 3x3

## Quoi faire ?

Ecrire un programme python qui résoud une ou plusieurs grilles de sudoku. La question intéressante : peut-on, en appliquant diverses techniques de simplification, se passer du backtrack (retour arrière) ?

- Voici un site listant les techniques possible : [Hudoku](http://hodoku.sourceforge.net/en/techniques.php)
- Plus de détails sur le sudoku : [sudoku par wikipédia](https://fr.wikipedia.org/wiki/Sudoku)

## Contributions

- Sébastien Hoarau : pour l'instant je ne mets pas encore mon code que j'ai récupéré d'un vieux programme que j'avais fait il y a plusieurs années et qui est loin d'être propre. 
Mes stats : 
	- Sans backtrack : 26318 grilles, temps moyen : 0.007s
	- Avec backtrack : 22833 grilles, temps moyen : 0.034s
