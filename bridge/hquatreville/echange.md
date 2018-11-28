

27/11/2018 23:30 <br> 
SVP mettre un message dans issue qui devrait normalement m'envoyer un mail qd vous voulez me dire qque chose (question ou nouveau code à tester)<br>

Je vois que vous posez une question sur le pb des performances du code qd vous testez les donnes avec le filtre. Si je comprends votre code, vous lancez des donnes aléatoires dont vous testez la validité par rapport aux filtres. Je ne sais pas ce qu'est la part de temps du passage de la donne dans le filtre (j'ai juste vu vos tests imbriqués de loin) mais je suppose que la recherche aléatoire de la bonne donne doit etre le point noir. Ne pourriez vous orienter le hasard en prédeterminant les donnes aleatoires :

- si vous voulez 6 carreaux : pourquoi ne pas prendre au hasard 6 carreaux parmi 13, puisque de toutes facons c'est ce que vous voulez, ensuite c'est vous qui voyez pour remettre les 7 carreaux restants entre les 3 autres joueurs ou pour les remettre dans le pot commun à répartir. 
- si le filtre demande x points sur un joueur, c'est moins net mais vous pouvez sans doute orienter dans le choix des cartes qui peuvent donner les points attendus après le bilan des filtres de couleurs.  
- donc en gros il me semble que si vos préchoix respectent les critères, vous seriez moins en difficulté.


la piste me semble correcte.

Du point de vue informatique, il s'agit d'implémenter une méthode distribue à l'objet Sequence qui crée une donne. 
Et c'est cette méthode qu'il faudra optimiser.

D'un point de vue algorithmique, le problème est sérieux, il faut commencer par analyser les filtres pour les regrouper par couleurs.
Et ensuite, il faut faire super-gaffe de ne pas bieaiser les probabilités.

Super intéressant, mais pas urgent. Améliorer l'ergonomie générale pour éviter que les partenaires ne ralent ... Ensuite utiliser un truc du genre cx-freeze (je ne sais pas ce qui est le mieux mais c'est celui que google cite le plus...) pour les non utilisateurs de python.


