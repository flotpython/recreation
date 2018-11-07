"""
Le module qui gère la résolution d'un sudoku
C'est ce module qui code les différentes techniques
en s'appuyant sur la partie struct_sudoku pour
la demande des diverses vues 
Le module fait remonter les modifs à la partie structurelle
Les techniques de simplification / résolution sont décrites 
dans le site : http://hodoku.sourceforge.net/en/techniques.php
"""

import time
import struct_sudoku as sts



MOD = sts.MOD
SIZE = sts.SIZE
HOUSES_TYPES = sts.HOUSES_TYPES
NUMBERS = sts.NUMBERS
BLOCK = sts.BLOCK
ROW = sts.ROW
COL = sts.COL

TECHNIQUES = ['naked_single', 'hidden_single',
            'intersections',
            'hidden_subsets',
            'naked_subsets',
            'basic_fish', 
            'xy-wing',
            'w-wing',]

# Pour dessiner les bordures de la grille
#
TLC = '\u250C'  # Top Left Corner
TIB = '\u252C'  # Top Inner Border
TRC = '\u2510'  # Top Right Corner
MLB = '\u251C'  # Middle Left Border
MIB = '\u253C'  # Middle Inner Border
MRB = '\u2524'  # Middle Right Border
BLC = '\u2514'  # Bottom Left Corner
BIB = '\u2534'  # Bottom Inner Border
BRC = '\u2518'  # Bottom Right Corner
SBO = '\u2500'  # Simple BOrder
VSEP = '|' # Vertical Line

# Les lignes pour dessiner la grille
#
TOP = f'{TLC}{SBO * 7}{TIB}{SBO * 7}{TIB}{SBO * 7}{TRC}'
MIDDLE = f'{MLB}{SBO * 7}{MIB}{SBO * 7}{MIB}{SBO * 7}{MRB}'
BOTTOM = f'{BLC}{SBO * 7}{BIB}{SBO * 7}{BIB}{SBO * 7}{BRC}'



class Sudoku:

    def __init__(self, id_sudoku, data):
        self.id = id_sudoku     # identifiant de la grille
        self.data = data        # la ligne de données de la grille
        self.temps = 0          # temps mis pour résoudre
        self.solved = False # Une solution été trouvée
        self.sudoku = sts.Sudoku(data) # la partie structurelle du sudoku
        self.techniques = {tech:0 for tech in TECHNIQUES}
        self.techniques['backtracking'] = 0

    def __repr__(self):
        """ Affichage d'un beau sudoku avec bordure sympa """
        etat = 'résolue' if self.solved else 'initiale'
        chaine = f'\nGrille {self.id} {etat}\n'
        chaine += f'{TOP}\n'
        for cell in self.sudoku.cells:
            symbol = '.' if cell.empty() else str(cell.val)
            if cell.row > 0 and cell.id % (SIZE * MOD) == 0:
                chaine += f'{MIDDLE}\n'
            if cell.col % MOD == 0:
                chaine += f'{VSEP} '
            chaine += f'{symbol} '
            if (cell.col + 1) % SIZE == 0:
                chaine += f'{VSEP}\n'
        chaine += f'{BOTTOM}\n'
        return chaine


    # -- small functions --

    def _code(self, row, col):
        return row * SIZE + col

    def _decode(self, cell_id):
        return cell_id // SIZE, cell_id % SIZE

    # -- Pour debugguer

    def debug(self):
        """ 
        Permet d'afficher un sudoku pour debuggage :
        chaque cellule est affichée soit avec sa valeur unique
        soit avec l'ensemble de ces candidats
        """
        s = ''
        for row in range(SIZE):
            if row > 0 and row % MOD == 0:
                s += '-'*47+'\n'
            else:
                s += '\n'
            for ligne in range(3):                
                candidats = range(ligne*3+1, ligne*3+4)
                for col in range(SIZE):
                    cell_id = self._code(row, col)
                    cell = self.sudoku.cells[cell_id]
                    if col > 0 and col % MOD == 0:
                        s += f'{VSEP} '
                    if not cell.empty():
                        if ligne == 1:
                            s += f'|{cell.val}|  '
                        else:
                            s += '     '
                    else:
                        tmp = ''
                        for c in candidats:
                            if c in cell.candidats:
                                tmp += f'{c}'
                            else:
                                tmp += '.'
                        s += f'{tmp}  '
                s += '\n'
        print(s)




    # --
    # -- INFORMATIONS
    # --

    def cell(self, cell_id):
        """ La cellule d'ID cell_id """
        return self.sudoku.cells[cell_id]

    def candidats(self, cell_id):
        """ Les candidats de la cellule cell_id """
        return self.cell(cell_id).candidats

    def house(self, house_type, house_id):
        """ 
        La maison de type house_type (0, 1, ou 2) et
        d'ID house_id
        """
        return self.sudoku.house(house_type, house_id)

    def empty_cells(self):
        """ L'ensemble des cellules vides """
        return self.sudoku.empty_cells

    def empty_ids(self):
        """ L'ensemble des ID des cellules vides """
        return self.sudoku.empty_ids()


    def visible_cell_ids(self, cell_id):
        """ ID des cellules visibles par la cellule cell_id """
        return self.sudoku.visible_cell_ids(cell_id)


    def full(self):
        return len(self.sudoku.empty_cells) == 0

    # --
    # -- UPDATE METHODS
    # --

    # Grosso modo il existe 2 update possibles :
    # mettre une valeur n dans une cellule (et propager)
    # retirer un candidat de l'ensemble des candidats d'une cellule
    # ces update sont demandés à la partie struct

    def set_cell(self, cell, val):
        self.sudoku.set_cell(cell, val)

    def reset_cell(self, cell):
        self.sudoku.reset_cell(cell)

    def remove_empty(self, cell):
        self.sudoku.remove_empty(cell)

    def first_empty(self):
        return self.sudoku.first_empty()

    def insert_cell(self, cell):
        self.sudoku.insert_cell(cell)

    def try_remove(self, cell_id, candidat, tech):
        try:
            self.cell(cell_id).remove_candidat(candidat)
        except:
            return False
        else:
            if tech:
                self.techniques[tech] += 1
            return True


    # --
    # -- SIMPLIFICATION METHODS
    # --


    # -- NAKED SINGLE --

    def naked_single(self):
        """
        Si pour une case vide (x,y) il n'y a qu'une
        seule possibilité alors on joue cette valeur
        """
        found = False
        for cell in self.empty_cells():
            if cell.singleton():
                val = cell.candidats.pop()
                self.remove_empty(cell)
                self.set_cell(cell, val)

                found = True
                self.techniques['naked_single'] += 1
        return found


    # -- HIDDEN SINGLE --

    def hidden_single(self):
        found = False
        for house_type in HOUSES_TYPES:
            for house_id in range(SIZE):
                house = self.house(house_type, house_id)
                for n in NUMBERS:
                    id_positions = house.ids_for_n(n)
                    if len(id_positions) == 1:
                        cell = self.cell(id_positions.pop())
                        found = True
                        self.techniques['hidden_single'] += 1
                        self.set_cell(cell, n)
                        self.remove_empty(cell)
        return found


    # -- INTERSECTIONS --

    def intersections(self):
        """ Implemente Locked candidats type 1 et 2 """
        found = False
        for block_id in range(SIZE):
            house = self.house(BLOCK, block_id)
            for n in house.candidats():
                block_ids = house.ids_for_n(n)
                for lig_col_id in range(SIZE):
                    house_row = self.house(ROW, lig_col_id)
                    house_col = self.house(COL, lig_col_id)
                    row_ids = house_row.ids_for_n(n)
                    col_ids = house_col.ids_for_n(n)
                    inter_row = block_ids & row_ids
                    inter_col = block_ids & col_ids
                    if inter_row:
                        inter = inter_row
                    elif inter_col:
                        inter = inter_col
                    else:
                        inter = set()
                    if inter:
                        if inter < row_ids and inter == block_ids:
                            cells_to_update = row_ids - inter
                        elif inter < block_ids and inter == row_ids:
                            cells_to_update = block_ids - inter
                        else:
                            cells_to_update = set()
                        for cell_id in cells_to_update:
                            found = self.try_remove(cell_id, n, 'intersections') or found
                if found:
                    return found
        return False



    # -- HIDDEN SUBSETS --

    def hidden_subsets(self, k):
        found = False
        for house_type in HOUSES_TYPES:
            for house_id in range(SIZE):
                found, ok = False, False
                house = self.house(house_type, house_id)
                if len(house.empty_ids()) > k:
                    # dans la boucle qui suit on crée 2 ensembles :
                    # set_n un ensemble de candidats 
                    # set_cell l'ensemble d'id de cellules qui partagent ces
                    # candidats
                    # si les deux coïncident en taille avec k alors on peut
                    # retirer les autres candidats des cellules en question
                    #
                    for n in house.candidats():
                        set_n = {n}
                        set_cell = house.ids_for_n(n)
                        if len(set_cell) <= k:
                            for m in house.candidats() - {n}:
                                set_cell_m = house.ids_for_n(m)
                                if set_cell & set_cell_m:
                                    union = set_cell | set_cell_m
                                    if len(union) <= k:
                                        set_cell = union
                                        set_n.add(m)
                                if len(set_cell) == k and len(set_n) == k:
                                    ok = True
                                    break
                            if ok:
                                break
                    if ok:
                        for cell_id in set_cell:
                            cell = self.cell(cell_id) 
                            if cell.candidats > set_n:
                                found = True
                                cell.candidats = cell.candidats & set_n 
                    if found:
                        self.techniques['hidden_subsets'] += 1
                        return found
        return found


    # -- NAKED SUBSETS --

    def naked_subsets(self, k):
        found = False
        # on parcourt les maisons
        for house_type in HOUSES_TYPES:
            for house_id in range(SIZE):
                found, ok = False, False
                house = self.house(house_type, house_id)
                # on récupère les cellules vides de cette maison
                empty_cells = house.empty_ids() 
                if len(empty_cells) > k:  # si suffisamment de cellules vides y'a peut-être qqc à faire
                    # dans la boucle qui suit on crée 2 ensembles :
                    # set_cell un ensemble d'id de cellules
                    # set_n l'ensemble des candidats communs pour ces cellules
                    # si les deux coïncident en taille avec k alors on peut
                    # retirer des autres cellules de la maison les candidats en question
                    for cell_id in empty_cells:
                        set_n = self.cell(cell_id).candidats
                        if len(set_n) <= k:
                            set_cell = {cell_id}
                            for cell_id_2 in empty_cells - {cell_id}:
                                set_n_2 = self.cell(cell_id_2).candidats
                                if set_n & set_n_2:
                                    union = set_n | set_n_2
                                    if len(union) <= k:
                                        set_n = union
                                        set_cell.add(cell_id_2)
                                if len(set_n) == k and len(set_cell) == k:
                                    ok = True
                                    break
                            if ok:
                                break
                    if ok:
                        for cell_id in empty_cells - set_cell:
                            cell = self.cell(cell_id)
                            if set_n < cell.candidats:
                                found = True
                                cell.candidats = cell.candidats - set_n 
                    if found:
                        self.techniques['naked_subsets'] += 1
                        return found
        return found
    
    
    # -- BASIC FISH --

    def k_row_cols(self, house_type, k):
        d_cells_ids = {}
        for n in NUMBERS:
            d_cells_ids[n] = [set() for _ in range(SIZE)]
            for coord_id in range(SIZE):
                house = self.house(house_type, coord_id)
                cells_ids = house.ids_for_n(n)
                if 1 < len(cells_ids) <= k:
                    d_cells_ids[n][coord_id] = {self._decode(cell_id)[1 - house_type] for cell_id in cells_ids}
        return d_cells_ids


    def k_fusion(self, l_cells_ids, k):
        for index, cols in enumerate(l_cells_ids):
            set_rows = {index}
            set_cols = cols
            for index2, cols2 in enumerate(l_cells_ids):
                if index2 != index and set_cols & cols2:
                    union = set_cols | cols2
                    if len(union) <= k:
                        set_cols = union
                        set_rows.add(index2)
                    if len(set_cols) == k and len(set_rows) == k:
                        return set_rows, set_cols    
        return set(), set()    



    def basic_fish(self, k):
        found = False
        for house_type in [ROW, COL]:
            d_cells_ids = self.k_row_cols(house_type, k)
            for n in d_cells_ids:
                set_rows, set_cols = self.k_fusion(d_cells_ids[n], k)
                if set_rows:
                    if house_type == COL:
                        set_rows, set_cols = set_cols, set_rows
                        for col_id in set(range(SIZE)) - set_cols:
                            for row_id in set_rows:
                                found = self.try_remove(self._code(row_id, col_id), n, 'basic_fish') or found
                    else:
                        for row_id in set(range(SIZE)) - set_rows:
                            for col_id in set_cols:
                                found = self.try_remove(self._code(row_id, col_id), n, 'basic_fish') or found

                if found:
                    return True
        return False

 
    
    # -- XY-WINGS --

    def get_pivot(self):
        return {(cell.id,) + tuple(self.candidats(cell.id)) 
                    for cell in self.empty_cells() 
                    if len(self.candidats(cell.id)) == 2}

    def get_pincers(self, pivot, set_xy):
        # print(f'Pivot {self.cell(pivot).row},{self.cell(pivot).col} XY {set_xy}')
        for cell_id_2 in self.visible_cell_ids(pivot):
            pincers = set()
            z = None
            x = self.candidats(cell_id_2) & set_xy
            list_z = list(self.candidats(cell_id_2) - set_xy)
            if  len(list_z) == 1 and len(x) == 1:
                pincers.add(cell_id_2)
                z = list_z[0]
                # print(f'inter {x} {self.cell(cell_id_2).row},{self.cell(cell_id_2).col} {list_z}')

                for cell_id_3 in self.visible_cell_ids(pivot) - {cell_id_2}:
                    y = self.candidats(cell_id_3) & set_xy
                    list_z_3 = list(self.candidats(cell_id_3) - set_xy)
                    # print(f'\tinter {y} {self.cell(cell_id_3).row},{self.cell(cell_id_3).col} {list_z_3} z {z}', end='...')
                    if len(y) == 1 and x != y and len(list_z_3) == 1 and list_z_3[0] == z:
                        pincers.add(cell_id_3)
                        # input('yes')
                        return pincers, z
                    # else:
                    #     print('no')
        return set(), None


    def xy_wing(self):
        found = False
        for cell_id, x, y in self.get_pivot():
            pincers, z = self.get_pincers(cell_id, {x, y})
            if not z is None:
                if len(pincers) == 2:
                    cell_id_2, cell_id_3 = pincers
                    cells_to_update = self.visible_cell_ids(cell_id_2) & self.visible_cell_ids(cell_id_3) - pincers - {cell_id}
                    for other_cell_id in cells_to_update:
                        found =  self.try_remove(other_cell_id, z, 'xy-wing') or found
                    if found:
                        return True
        return False



    # -- W-WING --

    def get_bivalues(self):
        return {(cell_id_1, cell_id_2) for cell_id_1 in self.empty_ids() 
                    for cell_id_2 in self.empty_ids() 
                    if self._decode(cell_id_1)[0] != self._decode(cell_id_2)[0] and 
                    self._decode(cell_id_1)[1] != self._decode(cell_id_2)[1] and
                    self.candidats(cell_id_1) == self.candidats(cell_id_2) and
                    len(self.candidats(cell_id_1)) == 2 
                    }

    def get_lock(self, house_type, cell_id_1, cell_id_2):
        rowcol_id_1 = self._decode(cell_id_1)[house_type]
        rowcol_id_2 = self._decode(cell_id_2)[house_type]
        candidats = self.candidats(cell_id_1)
        locks_id = {(lock_id_1, lock_id_2) 
                    for lock_id_1 in self.house(house_type, rowcol_id_1).empty_ids()
                    for lock_id_2 in self.house(house_type, rowcol_id_2).empty_ids()
                        if self._decode(lock_id_1)[1 - house_type] == self._decode(lock_id_2)[1 - house_type]
                        and lock_id_1 != cell_id_1 and lock_id_1 != cell_id_2
                        and lock_id_2 != cell_id_1 and lock_id_2 != cell_id_2} 
        for lock_id_1, lock_id_2 in locks_id:
            l_locked_value = list(self.candidats(lock_id_1) & candidats)
            if len(l_locked_value) == 1:
                c = l_locked_value[0]
                perpendiculaire = self._decode(lock_id_1)[1 - house_type]
                if len(self.house(1 - house_type, perpendiculaire).ids_for_n(c)) == 2:
                    return {lock_id_1, lock_id_2}, c
        return set(), None



    def w_wing(self):
        found = False
        for cell_id_1, cell_id_2 in self.get_bivalues():
            row_id_1, col_id_1 = self._decode(cell_id_1)
            row_id_2, col_id_2 = self._decode(cell_id_2)
            house_type = ROW
            lock_set, lock_value = self.get_lock(house_type, cell_id_1, cell_id_2)
            if not lock_set:
                house_type = COL
                lock_set, lock_value = self.get_lock(house_type, cell_id_1, cell_id_2)
            if lock_set:
                value_to_delete = list(self.candidats(cell_id_1) - {lock_value})[0]
                cells_to_update = self.visible_cell_ids(cell_id_1) & self.visible_cell_ids(cell_id_2)
                for cell_id in cells_to_update:
                    found = self.try_remove(cell_id, value_to_delete, 'w-wing') or found
                if found:
                    return True
        return False
    

    # -- MAIN SIMPLIFICATION METHOD --

    def simplify(self):
        """
        Essaie de simplifier une grille en utilisant les
        techniques classiques décrites dans 
        http://hodoku.sourceforge.net/en/techniques.php
        """
        change = True
        while not self.full() and change:
            change = False
            change = self.naked_single() or change
            change = self.hidden_single() or change
        
            if not self.full() and not change:
                change = self.intersections()


            if not self.full() and not change:
                for k in range(2,5):
                    change = self.hidden_subsets(k) or change
                    if change:
                        break

            if not self.full() and not change:
                for k in range(2,5):
                    change = self.naked_subsets(k) or change
                    if change:
                        break

            if not self.full() and not change:
                for k in range(2,5):
                    change = self.basic_fish(k) or change
                    if change:
                        break

            if not self.full() and not change:
                change = self.xy_wing()

            if not self.full() and not change:
                change = self.w_wing()


        if self.full():
            self.solved = True


    # --
    # -- BACKTRACK
    # --

    def sort_empty_cells(self):
        self.empty_cells().sort(key=lambda e:len(e.candidats))


    def solve_by_backtracking(self):
        if self.full():
            return True
        else:
            self.sort_empty_cells()
            cell = self.first_empty()
            memory = [] # pour mémoriser les candidats (pour les remettre)
            while cell.candidats:
                e = cell.candidats.pop()
                memory.append(e)
                self.set_cell(cell, e)
                self.techniques['backtracking'] += 1
                if self.solve_by_backtracking():
                    return True
                else:
                    self.reset_cell(cell)
                    self.techniques['backtracking'] -= 1
            # On est dans une impasse : on remet cette case vide en case vide
            # avec ses candidats avant de retourner False pour dire au-dessus 
            # qu'on est bloqué
            cell.candidats.update(memory)
            self.insert_cell(cell)
            return False
    
    
    # --
    # -- MAIN SOLVE METHOD
    # --

    def solve(self):
        """
        La méthode pour résoudre le sudoku :
        1. d'abord en appliquant diverses méthodes de simplification
        2. par backtracking
        """
        self.temps = time.time()
        self.simplify()
        self.solved = self.solve_by_backtracking()
        self.temps = time.time() - self.temps



    # --
    # -- STATS
    # --

    def analyse(self):
        print(self)
        nbcar = max(len(s) for s in TECHNIQUES) + 2
        print(f'Statistiques pour {self.id}')
        print('----')
        total = 0
        for technique in TECHNIQUES:
            total += self.techniques[technique]
            print(f'{technique:{nbcar}} : {self.techniques[technique]:2} résolutions')
        print(f'{"TOTAL":{nbcar}} : {total:2} résolutions')
        print('----')
        print(f'Par backtracking : {self.techniques["backtracking"]} cases.')
        if self.solved:
            print(f'Au final, grille résolue en {self.temps:.3f}s')
        else:
            print('Au final, grille non résolue.')
        print('----\n')


