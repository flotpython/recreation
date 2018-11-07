"""
Modélise la structure d'un sudoku
Un sudoku c'est une collection de Cellules,
regroupées en Houses (Row, Col, Block)

La structure doit pouvoir fournir :
-   une case (Cell) individuelle si on connait son id ou
    ses coordonnées id_row, id_col
-   un set de cases par House
-   un set des cases dans la même House qu'une case
-   etc.

TODO : l'ensemble manque encore de cohérence. 

Auteur  : Sébastien Hoarau
Date    : 2018.11.01
"""

# --
# -- CONSTANTES
# --

SIZE = 9
MOD = 3
ALL = SIZE ** 2


ROW = 0
COL = 1
BLOCK = 2

HOUSES_TYPES = [ROW, COL, BLOCK]
HOUSES_RANGE = [
    lambda i: range(i*SIZE,i*SIZE+SIZE),
    lambda i: range(i,i+(SIZE*SIZE - SIZE)+1,SIZE),
    lambda i: (row*SIZE+col for row in range((i//MOD)*MOD, (i//MOD)*MOD+MOD) 
                    for col in range((i%MOD)*MOD, (i%MOD)*MOD+MOD)) 
    ]

EMPTY = 0
NUMBERS = set(range(1,SIZE+1))


# --
# -- LES CLASSES
# --

class Cell:
    """
    Une cellule de sudoku
    """

    def __init__(self, cell_id, val):
        self.id = cell_id           # un numéro entre 0 et ALL-1 (80)
        self.row = cell_id // SIZE  # numéro de ligne entre 0 et SIZE   
        self.col = cell_id % SIZE   # numéro de colonne
        self.block = (self.row // MOD) * MOD + self.col // MOD # numéro de block
        self.val = val
        self.houses = [self.row, self.col, self.block]
        self.candidats = set()
        self.impacted = set() # cellules impactées par remplissage de la cell

    def __repr__(self):
        return f'{self.row},{self.col}'

    def house(self, house_type):
        return self.houses[house_type]

    # -- informations methods --

    def empty(self):
        return self.val == EMPTY

    def singleton(self):
        return len(self.candidats) == 1

    def coord(self, row_or_col):
        return [self.row, self.col][row_or_col]

    # -- update methods --

    def set_val(self, val):
        self.val = val

    def reset_val(self):
        while self.impacted:
            cell = self.impacted.pop()
            cell.candidats.add(self.val)
        self.val = EMPTY

    def remove_candidat(self, n):
        self.candidats.remove(n)

    def add_impacted(self, cell):
        self.impacted.add(cell)



class House:
    """
    Les maisons sont les regroupements de 9 cellules :
    en ligne, colonne et bloc de 3x3
    Elles ont un type 0 pour les lignes, 1 pour les col
    et 2 pour les blocs, et un identifiant (0 à 8)
    Et bien sûr un ensemble de cellules (directement les
    cellules mais aussi leurs ID)

    TODO : clarifier l'utilisation des cellules. A mon avis
    on peut manipuler *que* les ID Globalement ça manque encore
    de cohérence entre solve_sudoku et struct_sudoku
    """

    def __init__(self, sudoku, house_type, house_id):
        self.id = house_id
        self.type = house_type
        self.sudoku = sudoku
        self.cells_id = set(HOUSES_RANGE[self.type](self.id))
        self.cells = {sudoku.cells[cell_id] for cell_id in self.cells_id}

        
    def candidats(self):
        return {n for n in NUMBERS - {cell.val for cell in self.cells}}

    def empty_ids(self):
        return {cell_id for cell_id in self.cells_id if self.sudoku.cells[cell_id].empty()}

    def ids_for_n(self, n):
        return {cell_id for cell_id in self.empty_ids() if n in self.sudoku.cells[cell_id].candidats}


class Sudoku:
    """
    La structure de sudoku, avec ses cellules, ses maisons
    etc.
    """

    def __init__(self, data):
        self.cells = []             # la liste des ALL cellules
        self.empty_cells = []       # doit être une liste pour pouvoir trier
        self.houses = [[],[],[]]    # la liste des MOD x SIZE maisons

        # Création des cellules
        #
        for cell_id, v in enumerate(data):
            v = int(v)
            cell = Cell(cell_id, v)
            self.cells.append(cell)
            if v == EMPTY:
                self.empty_cells.append(cell)
                cell.candidats = {n for n in NUMBERS}

 
        # Création des maisons
        #
        for house_type in HOUSES_TYPES:
            for house_id in range(SIZE):
                self.houses[house_type].append(House(self, house_type, house_id))
        self.propage()

    


    # -- FAIRE LES UPDATE --

    def cell_propage(self, cell):
        v = cell.val
        impacted_ids = self.visible_cell_ids(cell.id)
        for cell_id in impacted_ids:
            impacted_cell = self.cells[cell_id]
            try:
                impacted_cell.remove_candidat(v)
            except KeyError: 
                pass
            else:
                cell.add_impacted(impacted_cell)
    
    def propage(self):
        """
        Propage l'information du contenu des cellules
        pour retirer les candidats déjà pris dans chaque maison
        """
        for cell in self.cells:
            if not cell.empty():
                self.cell_propage(cell)

    def set_cell(self, cell, val):
        cell.set_val(val)
        self.cell_propage(cell)

    def reset_cell(self, cell):
        cell.reset_val()

    def remove_empty(self, cell):
        self.empty_cells.remove(cell)

    def first_empty(self):
        return self.empty_cells.pop(0)

    def insert_cell(self, cell):
        self.empty_cells.insert(0, cell)


    # -- DELIVRER LES INFORMATIONS --

    def empty_ids(self):
        return {cell.id for cell in self.empty_cells}
    
    def house(self, house_type, house_id):
        return self.houses[house_type][house_id]


    def visible_cell_ids(self, cell_id):
        """
        Toutes les id de cellules qui voient la cellule cell_id
        et différente d'elle bien sûr
        """
        seen_ids = set()
        for house_type, house_id in enumerate(self.cells[cell_id].houses):
            seen_ids = seen_ids | self.house(house_type, house_id).empty_ids()
        seen_ids -= {cell_id}
        return seen_ids


