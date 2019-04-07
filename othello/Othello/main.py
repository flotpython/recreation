import tkinter as tk
import game

root = tk.Tk()
jeu = game.Game(master=root)
jeu.master.title('Othello')
jeu.mainloop()
       

