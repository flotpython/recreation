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
        # tranche = table[l][c]
        if direction == 'E':
            tranche = table[l, c:]
        elif direction == 'W':
            tranche = table[l, :c+1]
        elif direction == 'N':
            tranche = table[:l+1, c]
        elif direction == 'S':
            tranche = table[l:, c]
        elif direction == 'SE':  # Utiliser np.ix_
            tranche = table[l:, c:]
        elif direction == 'SW':
            tranche = table[l:, :c+1]
        elif direction == 'NE':
            tranche = table[:l+1, c:]
        elif direction == 'NW':
            tranche = table[:l+1, :c+1]
        # tranche = np.array(tranche)
        print((direction, tranche))
        return tranche
        
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
            - index donnes l'index dans la tranche du dernier jeton à retourner
        """
        descr = (False, 0)
        if self.tranche[0] != 0:
            pass
        elif couleur in self.tranche[1:]:
            index = self.tranche[1:].index(couleur) + 1
            if index > 1 and not 0 in self.tranche[1:index]:
                descr = (True, index)          
        return descr

        
        
        