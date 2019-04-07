import tkinter as tk
import othello as oth

class Couleurs(dict):    
    def __missing__(self, key):
        return 'yellow'

couleurs = Couleurs()
couleurs[oth.NOIR]='Red'
couleurs[oth.BLANC]='Green'
couleurs[oth.VIDE]='White'

sizeV = oth.SIZE
sizeH = len(oth.COLONNES)
zoom = 20

class Game(tk.Frame):
    def __init__(self, master=None, couleur=oth.NOIR):
        tk.Frame.__init__(self, master)
        self.master = master
        self.jeu = oth.Othello()
        self.joueur = couleur
        self.create_widgets()

    def jouer(self, event):
        # if self.joueur == self.jeu.joueur: #si c'est au tour de l'humain de jouer
            ligne = int((event.x - zoom)/zoom)
            colonne = int((event.y - zoom)/zoom)
            self.jeu.playJoueur(ligne, colonne)   
        # else:
            # self.jeu.playAI()
            self.drawtable(self.jeu.jeu)   
        
    def next(self):
        self.jeu.playAI()
        self.drawtable(self.jeu.jeu)

    def nouveau_jeu(self):
        """ Commence une nouvelle partie avec l'autre couleur """
        self.label_couleur_couleur.destroy()
        self.__init__(master=self.master, couleur=-self.joueur)
        if self.joueur != self.jeu.joueur:
            self.jeu.playAI()
            self.drawtable(self.jeu.jeu)
        
    def help(self):
        hilfe = self.jeu.casesJouables(self.jeu.joueur)
        self.drawtable(hilfe)

    def score(self):
        return self.jeu.score()

    def drawtable(self, table):
        for l in range(oth.SIZE):
            for k in range(len(oth.COLONNES)):
                rec = self.C.create_rectangle((l+1)*zoom, (k+1)*zoom, (l+2)*zoom, (k+2)*zoom, tag='case')
                cir = self.C.create_oval((l+1)*zoom, (k+1)*zoom, (l+2)*zoom, (k+2)*zoom, fill=couleurs[table[l][k]])
        self.label_score.destroy()
        gagnant = oth.NOIR if self.score()[0]>=self.score()[1] else oth.BLANC
        self.label_score = tk.Label(self.master,
                                    text=f'{couleurs[oth.NOIR]}={self.score()[0]}|{couleurs[oth.BLANC]}={self.score()[1]}',
                                    bg=couleurs[gagnant])
        self.label_score.grid(row=sizeV+6, column=1)

    def create_widgets(self):
        ### Définition des widgets
        self.C = tk.Canvas(self.master, width=(len(oth.COLONNES)+2)*zoom,
                           height=(oth.SIZE+2)*zoom, bg='white')
        self.bouton_quit = tk.Button(self.master, text='Quitter', fg='red',
                                     command=self.master.destroy)
        self.label_couleur_info = tk.Label(self.master, text='Votre couleur: ')
        self.label_couleur_couleur = tk.Label(self.master,
                                              text=couleurs[self.joueur],
                                              bg=couleurs[self.joueur])
        self.bouton_nouveau = tk.Button(self.master, text='Changez votre couleur', command=self.nouveau_jeu)
        self.bouton_help = tk.Button(self.master, text='Help', command=self.help)
        gagnant = oth.NOIR if self.score()[0]>=self.score()[1] else oth.BLANC
        self.label_score = tk.Label(self.master,
                                     text=f'{couleurs[oth.NOIR]}={self.score()[0]}|{couleurs[oth.BLANC]}={self.score()[1]}',
                                     bg=couleurs[gagnant])                     
        self.bouton_AI = tk.Button(self.master, text='AI', command=self.next)

        ### Placement des widgets
        self.C.grid(row=1, column=1, rowspan=sizeV+2, columnspan=sizeH+2, padx=5, pady=5)
        self.bouton_AI.grid(row = sizeV+3, column=1)
        self.label_couleur_info.grid(row=sizeV+4, column=1, sticky=tk.W)
        self.label_couleur_couleur.grid(row=sizeV+5, column=1)
        self.label_score.grid(row=sizeV+6, column=1)
        self.bouton_nouveau.grid(row=sizeV+3, column=sizeH+2)
        self.bouton_help.grid(row=sizeV+4, column=sizeH+2)
        self.bouton_quit.grid(row=sizeV+6, column=sizeH+2)

        ## Le Canvas
        x, y = 3*zoom/2, zoom/2
        for a in oth.COLONNES:
            labelC = self.C.create_text(x, y, text=a)
            labelC2 = self.C.create_text(x, (sizeV+3/2)*zoom, text=a)
            x += zoom
        x, y = zoom/2, 3*zoom/2
        for i in oth.LIGNES:
            labelL = self.C.create_text(x, y, text=i)
            labelL2 = self.C.create_text( (sizeH+3/2)*zoom, y, text=i)
            y += zoom
        self.drawtable(self.jeu.jeu)

        ## Events
        self.C.bind('<Button-1>', self.jouer)



class Nouveau_Jeu(tk.Frame):
    def __init__(self, master=None, couleur=oth.NOIR):
        tk.Frame.__init__(self, master)
        self.master = master
        self.grid(ipadx=5, ipady=2)
        self.couleur = couleur
        self.create_widgets()

    def annul(self):
        self.master.destroy()

    def valid(self):  ####
        self.master.destroy()

    def to_noir(self):
        self.couleur = oth.NOIR

    def to_blanc(self):
        self.couleur = oth.BLANC

    def create_widgets(self):
        # Widgets
        self.label = tk.Label(self.master, text=f'Choisissez votre couleur:\n({couleurs[oth.NOIR]} commence)')
        coul = tk.IntVar()
        coul.set(self.couleur)
        self.choix_noir = tk.Radiobutton(self.master, text=couleurs[oth.NOIR],
                                         variable=coul, value=oth.NOIR, fg=couleurs[oth.NOIR],
                                         command=self.to_noir)
        self.choix_blanc = tk.Radiobutton(self.master, text=couleurs[oth.BLANC],
                                          variable=coul, value=oth.BLANC, fg=couleurs[oth.BLANC],
                                          command=self.to_blanc)
        self.annul = tk.Button(self.master, text='Annuler', command=self.annul)
        self.valider = tk.Button(self.master, text='Valider', command=self.valid)

        # Grid
        self.label.grid(row=1, column=1, columnspan=2)
        self.choix_noir.grid(row=2, column=1, sticky=tk.W)
        self.choix_blanc.grid(row=3, column=1, sticky=tk.W)
        self.annul.grid(row=4, column=2, padx=2, pady=5)
        self.valider.grid(row=4, column=3, padx=5, pady=5)

        
##
##root = tk.Tk()
##jeu = Game(master=root)
##jeu.master.title('Othello')
##jeu.mainloop()

