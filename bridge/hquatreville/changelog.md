Jeudi 8 novembre
le fichier bridge_debut.py a été scindé en deux parties

-> Une bibliothéque nommée bridgelib
a) Les variables gloabales ont été rattachées aux bonnes fonctions
b) La lisibilité a été améliorée

-> Un fichier bridge_test pas forcément très lisible mais vérifiant que les imports de la bibliothèque bridgelib fonctionnent correctement

Dimanche 11 novembre

-> La biblithèque bridlib a été modifiée conformément aux recommandations des commentaire

-> Creation d'un fichier bridgetk correspondant a un premier jet d'utilisation de tkinter
C'est un premier jet opérationnel mais sans intérêt,
tout est en désordre
Le ménage va être fait

Grosse déception :
La classe IntEnum est incompatible avec les commandes grid()
de Tkinter fg = un intEnum renvoie un message d'erreur indiquant qu'il souhaite un entier 

Lundi 11 novembre

-> Ajout de la classe Position dans le fichier bridgelib pour une gestion plus fluide des 4 mains

-> Gros nettoyage de fichier bridgetk, le nouveau bridgtk2 accompli les mêmes fonctionnalités
avec amélioration de la lisibilité et facilité d'extension
