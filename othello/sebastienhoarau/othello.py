"""
	Othello.py
	Auteur : Sébastien Hoarau
	Date : 2018-10-11
"""

SIZE = 8
NOIR = 0
BLANC = 1
VIDE = -1
LABELS = ['X', 'O', '.']
LETTRES = 'ABCDEFGH'
HUMAIN = 0
MACHINE = 1
QUIT = 'QUIT'

class Othello:

	def __init__(self):
		self.g = [[VIDE] * SIZE for _ in range(SIZE)]
		self.g[3][3] = BLANC
		self.g[3][4] = NOIR
		self.g[4][3] = NOIR
		self.g[4][4] = BLANC


	def __str__(self):
		letters_line = '  ' + ' '.join([c for c in LETTRES])
		s = letters_line
		for idl in range(SIZE):
			s += f'\n{idl} '
			for idc in range(SIZE):
				s += f'{LABELS[self.g[idl][idc]]} '
			s += f'{idl}'
		s += f'\n{letters_line}'
		return s 


	def check_position(self, pos):
		pass


class Game:

	def __init__(self):
		self.othello = Othello()
		self.players = None
		self.scores = [2, 2]
		self.player = NOIR
		self.game_over = False

	def __str__(self):
		s = '\n' + self.othello.__str__() + '\n'
		if self.game_over:
			if self.scores[NOIR] > self.scores[BLANC]:
				s += f'\n{LABELS[NOIR]} gagne !'
			elif  self.scores[NOIR] < self.scores[BLANC]:
				s += f'\n{LABELS[BLANC]} gagne !'
			else:
				s += f'\nPartie nulle.'
		return s

	def settings(self):
		print('Bienvenue sur OTHELLO')
		print('Qui joue ?')
		print(f'0. Humain {LABELS[NOIR]} vs Humain {LABELS[BLANC]}')
		print(f'1. Humain {LABELS[NOIR]} vs Machine {LABELS[BLANC]}')
		rep = ''
		while rep != 0 and rep != 1:
			try:
				rep = int(input('Votre choix : '))
			except:
				rep = ''
		self.players = (HUMAIN, rep)

	def get_position(self):
		def good_coord(c):
			return 'A' <= c[0] <= 'H' and 0 <= int(c[1]) <= 7

		print(f'{LABELS[self.player]} joue...')
		if self.players[self.player] == HUMAIN:
			r = input('Quelle position ? (quit pour arrêter) ').upper()
			while r != QUIT and (len(r) != 2 or not good_coord(r)):
				r = input('Pas compris... votre réponse : ')
			if r == QUIT:
				


	def quit(self):
		self.game_over = True

	def next_player(self):
		self.player = 1 - self.player

	def play(self):
		while not self.game_over:
			print(self)
			position = self.get_position()
			if position == QUIT:
				self.quit()
			else:
				if self.othello.check_position(position):
					print('Position invalide')
				else:
					self.next_player()


jeu = Game()
jeu.settings()
jeu.play()
print(jeu)
