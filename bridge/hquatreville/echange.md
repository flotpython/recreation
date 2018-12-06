Jeudi 6 /12/ 2018
J'ai testé les différents modes sans rencontrer de vrais pbs.<br>
J'ai juste eu un petit doute dans le menu distribuer qd je demande x donnes , je m'attendais à les sauvegarder aussitot , mais il me semble que j'ai du ressortir pour les sauvegarder, mais c'est peut etre le fonctionnement attendu.
Ensuite comme on en demande toujours plus , mais vous verrez avec vos partenaires ,qd on est dans le menu encherir , un rappel des sequences testées ou du nom de fichier.pak qui doit etre explicite serait peut etre utile pour ne pas memoriser tout, est ce que des affichages des points H/HL  de chacun seraient aussi utiles pour ne pas recompter à chaque fois ?

Je n'ai pas regardé le code , mais en tous cas avec mes donnes tests à 16 points et demande de 5 donnes , le temps est très raisonnable et sans incidents.
Bravo ,  bonne continuation

Lundi 3 décembre

La version 1.0 me semble fonctionner avec

Ajout d'un menu normal pour gérer les séquences préprogrammées

Refonte de la méthode de distribution des donnes beaucoup plus rapide

Ajout d'une petite base d'exemples de filtres et de séquences

Le projet arrive à son terme





29/11/2018
J'ai reproduit ces comportements :

6 cartes à coeur et 16H et plus en Sud
6 cartes à carreau et 16H et plus en Nord

De temps en temps, j'ai le message d'erreur "donnes rares" et la plupart du temps "filtres incompatibles"
C'est normal, la probabilté de ces donnes est inférieure à 1 pour 100 000


Ensuite j'ai testé
6 cartes à coeur et 6H et plus en Sud
6 cartes à carreau et 16H et plus en Nord

Lorsque j'ai demandé de distribuer 50 donnes, je n'en ai obtenu que 26 car ces donnes sont en effet peu probable.

Heureusement, ce n'est pas ce que devarit testé un bridgeur normal en priorité, mais bon, cela fait partie de mes attentes.

Je pourrai "résoudre" partiellement le problème en distribuant 1 000 000 donnes au lieu de  100 000 mais cela augmente le temps d'attente.

En conséquence, l'amélioration de la vitesse d'exécution de la distribution passe de "à faire" à "assez urgent".

J'ai repéré aussi qu'avant de sauvegardé, je ne controllait pas les le pack de donne existe déjà, ce qui n'est ni grave ni urgent.

28/11/2018 23:30<br>
J'ai vu de gros changements dans l'ergonomie , on sait où on est, c'est bien mieux<br>
Maintenant en ce qui concerne le comportement, j'ai voulu tester mes filtres favoris, 6Ca N et 6Co S et la distribution ne fonctionne pas . Au début je ne l'avais pas vu et j'ai donc pu sauvegarder un fichier de donnes qui n'avait en fait que votre donne de démarrage et quand j'ai voulu relancer la distribution des cartes, j'ai vu qu'il était marqué que les filtres étaient incompatibles<br>
Je pensais qu'il était surtout difficile de trouver une donne aléatoire respectant mes critères car outre les longueurs j'ai demandé 16 points pour N et 16 points pour S . Mais pour autant la sauvegarde de la main ne m'avait pas été interdite.
J'ai donc recommencé avec seulement 6 points en Sud et il m'est encore annoncé que les filtres sont incompatibles, là c'est plus douteux en terme de difficulté à trouver des donnes compatibles 

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


