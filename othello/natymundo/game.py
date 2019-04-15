import tkinter as tk
import othello as oth
import numpy as np

# un petit dictionnaire de couleurs (c'était pas joli noir et blanc)


class Couleurs(dict):   # pour définir une valeur par défaut
    def __missing__(self, key):
        return 'yellow'


couleurs = Couleurs()
couleurs[oth.NOIR] = 'Red'
couleurs[oth.BLANC] = 'Green'
couleurs[oth.VIDE] = 'White'

# des valeurs utiles
sizeV = oth.SIZE
sizeH = len(oth.COLONNES)
zoom = 30


class Game(tk.Frame):
    def __init__(self, master=None, couleur=oth.NOIR, table=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.jeu = oth.Othello(table)
        # self.joueur est la couleur du joueur physique, 
        # self.jeu.joueur est le joueur dont c'est le tour
        self.joueur = couleur
        self.create_widgets()

####  Les actions réalisées suite à des commandes sur les widgets  #####
    def jouer(self, event):  # activé par un clic sur la surface de jeu
        if self.jeu.joueur == self.joueur:
            ligne = int((event.x - zoom)/zoom)
            colonne = int((event.y - zoom)/zoom)
            case = self.jeu.playJoueur(ligne, colonne)
            if case:
                self.drawtable(self.jeu.jeu)
                self.set_label_case(case[0])
                if case[1]: # eog = true
                    self.message_box(f"Bravo!!!\n\
                    Vous avez gagné!\n\
                    \nVotre score: {self.score(self.joueur)}\
                    \n(le score de votre adversaire: {self.score(-self.joueur)}")
            else:
                self.set_label_case(f"La case {self.jeu.toString((ligne, colonne))}\nn'est pas jouable...")
        else:
            self.message_box(
                "Ce n'est pas votre tour\n\
                (veuillez cliquer sur le bouton 'AI')")

    def next(self):  # activé par le bouton 'AI'
        if self.jeu.joueur == -self.joueur:
            case = self.jeu.playAI()
            self.drawtable(self.jeu.jeu)
            self.set_label_case(case[0])
            if case[1]:
                self.message_box(f"Vous avez perdu\n\
                    \nVotre score: {self.score(self.joueur)}\
                    \n(le score de votre adversaire: {self.score(-self.joueur)})")
        else:
            self.message_box("C'est à vous de jouer...")
            
    def nouveau_jeu(self):  # activé par le bouton 'Changer de couleur'
        """ Commence une nouvelle partie avec l'autre couleur """
        self.label_couleur_couleur.destroy()
        self.label_score_score.destroy()
        self.label_case_case.destroy()
        self.__init__(master=self.master, couleur=-self.joueur)

    def help(self): # activé par le bouton 'Help'
        """ Fait apparaître les cases jouables """
        for l in range(oth.SIZE):
            for k in range(len(oth.COLONNES)):
                if not isinstance(self.jeu.brouillon[l][k], (int, np.int8)):
                    cir = self.C.create_oval(
                        (l+1)*zoom, (k+1)*zoom, (l+2)*zoom, (k+2)*zoom, fill=couleurs['x'])
 
####  Des petites fonctions utiles  #### 
    def scoreN(self):
        """ renvoie le score de oth.NOIR """
        return self.jeu.score()[0]

    def scoreB(self):
        """ renvoie le score de oth.BLANC """
        return self.jeu.score()[1]
        
    def score(self, couleur):
        """ renvoie le score du joueur de couleur donnée """
        return self.scoreN() if couleur == oth.NOIR else self.scoreB()

    def gagnant(self):
        """ renvoie la couleur du gagnant"""
        return oth.NOIR if self.scoreN() > self.scoreB() else oth.VIDE if self.scoreN() == self.scoreB() else oth.BLANC

#### L'interface de jeu : les widgets, les petites fenêtres, etc... ####
    def message_box(self, message):
        """
            pop une fenêtre avec le message à faire passere
            et un bouton ok qui détruit la fenêtre
        """
        m_box_root = tk.Tk()
        m_box = tk.Frame(master=m_box_root)
        m_box.master.title('Message')
        m_box.grid(ipadx=10, ipady=10)
        label_text = tk.Label(m_box, text=message)
        label_text.grid(row=1, column=1)
        bouton_ok = tk.Button(m_box, text='Ok', command=m_box_root.destroy)
        bouton_ok.grid(row=2, column=1)

    def set_label_case(self, text):
        """ Change le label de la dernière case jouée """
        self.label_case_case.destroy()
        self.label_case_case = tk.Label(self.master, text=text)
        self.label_case_case.grid(row=6, column=1, rowspan=3, columnspan=2)

    def set_label_score(self):
        """ Change le label de score """
        self.label_score_score.destroy()
        self.create_label_score()

    def create_label_score(self):
        """ Affiche le score """
        self.label_score_score = tk.Label(self.master,
           text=f'{couleurs[oth.NOIR]}={self.scoreN()}|{couleurs[oth.BLANC]}={self.scoreB()}',
           fg=couleurs[self.gagnant()])
        self.label_score_score.grid(row=4, column=1, columnspan=2)

    def drawtable(self, table):
        """
            Dessine la table de jeu dans le canvas,
            et met à jour le score
        """
        for l in range(oth.SIZE):
            for k in range(len(oth.COLONNES)):
                rec = self.C.create_rectangle(
                    (l+1)*zoom, (k+1)*zoom, (l+2)*zoom, (k+2)*zoom, tag='case')
                cir = self.C.create_oval(
                    (l+1)*zoom, (k+1)*zoom, (l+2)*zoom, (k+2)*zoom, fill=couleurs[table[l][k]])
        self.set_label_score()
        
    def draw_canvas(self, canvas):
        """
            Dessine les labels des lignes et des colonnes, 
            Puis dessine la table de jeu
        """
        x, y = 3*zoom/2, zoom/2
        for a in oth.COLONNES:
            labelC = canvas.create_text(x, y, text=a)
            labelC2 = canvas.create_text(x, (sizeV+3/2)*zoom, text=a)
            x += zoom
        x, y = zoom/2, 3*zoom/2
        for i in oth.LIGNES:
            labelL = canvas.create_text(x, y, text=i)
            labelL2 = canvas.create_text((sizeH+3/2)*zoom, y, text=i)
            y += zoom
        self.drawtable(self.jeu.jeu)
        
    def create_boutons(self):
        """ Les boutons utilisés """
        self.bouton_quit = tk.Button(
            self.master, text='Quitter', fg='red',
            command=self.master.destroy)
        self.bouton_nouveau = tk.Button(
            self.master, text='Nouvelle partie', 
            command=self.nouveau_jeu)
        self.bouton_help = tk.Button(       ## command à modifier pour s'activer le temps où le bouton est pressé
            self.master, text='Help', 
            command=self.help)
        self.bouton_AI = tk.Button(
            self.master, text='AI', fg=couleurs[-self.joueur], 
            command=self.next)
            
    def create_labels(self):
        """ Les differents labels de la fenêtre """
        self.label_couleur_info = tk.Label(self.master, text='Votre couleur: ')
        self.label_couleur_couleur = tk.Label(self.master,
                                              text=couleurs[self.joueur],
                                              bg=couleurs[self.joueur])
        self.label_score = tk.Label(self.master, text='SCORE: ')
        self.create_label_score()
        self.label_case = tk.Label(self.master, text='Dernière case jouée: ')
        self.label_case_case = tk.Label(self.master)
        
    def griding(self):
        """
            Placement des widgets avec tk.grid
        """
        self.C.grid(row=1, column=3, rowspan=sizeV+2,
                    columnspan=sizeH+2, padx=5, pady=5)
        self.bouton_AI.grid(row=sizeV+3, column=3, sticky=tk.W)
        self.label_couleur_info.grid(
            row=1, column=1, columnspan=2, sticky=tk.W)
        self.label_couleur_couleur.grid(row=2, column=1, columnspan=2)
        self.label_score.grid(row=3, column=1, columnspan=2, sticky=tk.W)
        self.bouton_nouveau.grid(row=sizeV+3, column=sizeH+3, sticky=tk.E)
        self.bouton_help.grid(row=sizeV+4, column=3, sticky=tk.W)
        self.bouton_quit.grid(row=sizeV+4, column=sizeH+3, sticky=tk.E)
        self.label_case.grid(row=5, column=1, columnspan=2, sticky=tk.W)
        self.rowconfigure(sizeV+4, pad=2)
        self.columnconfigure(sizeH+3, pad=2)
    
    def create_widgets(self):
        # Définition des widgets
        self.C = tk.Canvas(self.master, width=(len(oth.COLONNES)+2)*zoom,
                           height=(oth.SIZE+2)*zoom, bg='white')
        self.create_boutons()
        self.create_labels()
        self.draw_canvas(self.C)
        # Grid
        self.griding()
        # Events
        self.C.bind('<Button-1>', self.jouer)
