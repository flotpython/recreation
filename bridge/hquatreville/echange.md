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

27/11/2018 23:30 <br> 
SVP mettre un message dans issue qui devrait normalement m'envoyer un mail qd vous voulez me dire qque chose (question ou nouveau code à tester)<br>

Je vois que vous posez une question sur le pb des performances du code qd vous testez les donnes avec le filtre. Si je comprends votre code, vous lancez des donnes aléatoires dont vous testez la validité par rapport aux filtres. Je ne sais pas ce qu'est la part de temps du passage de la donne dans le filtre (j'ai juste vu vos tests imbriqués de loin) mais je suppose que la recherche aléatoire de la bonne donne doit etre le point noir. Ne pourriez vous orienter le hasard en prédeterminant les donnes aleatoires :

- si vous voulez 6 carreaux : pourquoi ne pas prendre au hasard 6 carreaux parmi 13, puisque de toutes facons c'est ce que vous voulez, ensuite c'est vous qui voyez pour remettre les 7 carreaux restants entre les 3 autres joueurs ou pour les remettre dans le pot commun à répartir. 
- si le filtre demande x points sur un joueur, c'est moins net mais vous pouvez sans doute orienter dans le choix des cartes qui peuvent donner les points attendus après le bilan des filtres de couleurs.  
- donc en gros il me semble que si vos préchoix respectent les critères, vous seriez moins en difficulté.

J'ai vu que vous avez pris en compte mes remarques, mais je n'ai pas encore testé 


