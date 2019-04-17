import numpy as np

class Tranche:
    """
    Une classe qui définit des 'tranches' 
    de table du jeu Othello 
    à partir d'une case donnée,
    dans une direction donnée
    et pour une couleur donnée (default = 1)
    """
    
    def __init__(self, table, case, direction):
        self.case = case
        self.direction = direction
        self.tranche = self.get_tranche(table, self.case, self.direction)
       # self.descr = self.description(couleur)
    
    def get_tranche(self, table, case, direction):
        """
        Renvoie une 'tranche' de la table à partir de la case donnée et dans la direction donnée
        """
        (l, c) = case
        if direction == 'E':
            tranche = table[l, c:]
        elif direction == 'W':
            tranche = table[l, :c+1]
        elif direction == 'N':
            tranche = table[:l+1, c]
        elif direction == 'S':
            tranche = table[l:, c]
        elif direction == 'SE':
            tranche = table[l:].diagonal(c)
        elif direction == 'SW':  # A revoir
            tranche = np.array([table[i, k] for i, k in zip(range(l, len(table)), range(c))])
            # print((case, tranche))
        elif direction == 'NE': # A revoir
            tranche = np.array([table[i, k] for i, k in zip(range(l+1), range(c, len(table)))])
        elif direction == 'NW': 
            tranche = table[:l].diagonal(c-l)
        return tranche
        
        ### inutile d'update: les basic-slices sont des vues, donc mises à jour automatiques!
    def update(self, table):
        """
        Mets à jour la tranche
        Renvoie la tranche complète
        """
        self.tranche = self.get_tranche(table, self.case, self.direction)
        return self
        
    def description(self, couleur):
        """"
        Donne les infos utiles de la tranche sur sa jouabilité.
        Renvoie (jouable, index) où:
            - jouable est un booléen qui informe sur la jouabilité de la case
            - index donne l'index dans la tranche du dernier jeton à retourner
        """
        descr = (False, 0)
        # if len(self.tranche)>0:
            # if self.tranche[0] != 0:
                # pass
            # elif couleur in self.tranche[1:]:
                # index = self.tranche[1:].tolist().index(couleur) + 1
                # if index > 1 and not 0 in self.tranche[1:index]:
                    # descr = (True, index)    
        return descr

        
        
        