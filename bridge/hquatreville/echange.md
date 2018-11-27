26/11 23:00  JPBAUJOT<br>
En fait, ce qui m'a sans doute perturbé sur les donnes qui respectent sur les filtres <br>
C'est que la première donne ne respecte pas le filtre (je reconnais que c'est marqué en bas , mais je n'avais pas remarqué)<br>

===> J'ai modifié ce comportement, globalement idiot, surtout en phase de test

avec 1 seul fitre en Nord , j'ai obtenu le résultat <br>
en demandant 6 carreaux en Nord et 6 coeurs en sud , je n'obtiens pas ces résultats dans les donnes <br>

===> C'est un disfonctionnement majeur
La méthode filtre de l'objet Sequence était fausse, je l'ai corrigé (non sans mal car c'est une imbrication de ET et de OU)

De plus, pas besoin d'un utilitaire de profilage pour comprendre que cette méthode est la seule source de ralentissement du programme et nécessite une optimisation 
en vitesse.

Des idées ?

Details :
Pour les menus, eventuellement séparer d'une touche vide les sous menus des retours aux menus <br>

===> C'est fait !

Pour la sauvegarde d'une donne , il n'y a pas de touche valider , eventuellement un commentaire pour dire de faire enter

===> C'est fait !
