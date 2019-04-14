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
        (a, b) = direction
        (l, c) = case
        tranche = [table[l][c]]
        if a==b==0:
            pass
        else:
            A, B = l+a, c+b
            while 0 <= A < len(table) and 0 <= B < len(table[l]):
                tranche.append(table[A][B])
                A += a
                B += b
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

        
        
        