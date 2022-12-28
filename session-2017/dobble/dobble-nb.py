# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Le jeu de dobble

# %% [markdown]
# ## présentation

# %% [markdown] cell_style="split"
# Le dobble est un jeu de cartes:
#
# * chaque carte possède huit symboles,
# * quelque soit une paire de cartes, elles ont en commun exactement un symbole

# %% [markdown] cell_style="split"
# ![dobble](dobble.png)

# %%
import matplotlib.pyplot as plt
# somehow ipympl will result in a JS error..
# %matplotlib notebook

# %% [markdown]
# ## données brutes

# %% [markdown] cell_style="center"
# On vous donne la liste des cartes, dans un ordre totalement aléatoire:

# %% cell_style="center"
# il y en a bien plus que ça, mais pour vous donner une idée:
# une carte par ligne
# !head -8 cards10.txt

# %%
# 2 jeux de données

FILENAME = ""
SYMBOLS_PER_CARD = 0

# computed later on
N_CARDS = 0
N_SYMBOLS = 0

def init08():
    global SYMBOLS_PER_CARD, FILENAME
    SYMBOLS_PER_CARD = 8
    FILENAME = "cards08.txt"

def init10():
    global SYMBOLS_PER_CARD, FILENAME
    SYMBOLS_PER_CARD = 10
    FILENAME = "cards10.txt"

init10()
init08()


# %% [markdown]
# ## construction du paquet de cartes

# %%
# une carte est un ensemble de symboles
# et un symbole est représenté par une simple chaine
class Card(set):
    """
    le modèle pour chaque carte du jeu
    """
    
    # on leur donne un numéro arbitraire
    # dans l'ordre du paquet 
    counter = 1
    
    def __init__(self, *args, **kwds):
        set.__init__(self, *args, **kwds)
        self.counter = Card.counter 
        Card.counter += 1
        
    def __repr__(self):
        return f"[{self.counter:2d}] " + set.__repr__(self)
    
    def __hash__(self):
        return self.counter
    def __eq__(self, other):
        return self.counter


# %%
def read_cards(filename):
    with open(filename) as f:
        return [Card(line.split()) for line in f]


# %% [markdown]
# Attention à ne pas utiliser juste `cards` parce que c'est un nom de variable qu'on va massivement utiliser

# %%
all_cards = read_cards(FILENAME)
N_CARDS = len(all_cards)
print(f"we have {len(all_cards)} big cards")

# %% [markdown]
# ### combien de symboles

# %%
from functools import reduce

# or_ is | so let us call it what it does on sets
from operator import or_ as union

symbols = reduce(union, all_cards, set())

# %%
N_SYMBOLS = len(symbols)
print(f"we have {N_SYMBOLS} symbols")

# %%
# la liste des symboles, un peu mise en forme
columns = 7
colwidth = 16

for i, symbol in enumerate(sorted(symbols)):
    print(f"{symbol:{colwidth}s}", end="")
    if (i+1) % columns == 0:
        print()

# %% [markdown]
# ## vérifications

# %% [markdown]
# #### toutes les cartes ont le bon nombre de symboles

# %%
for card in all_cards:
    if len(card) != SYMBOLS_PER_CARD:
        print(f"OOPS {card} -> {len(card)}")

# %% [markdown]
# #### exactement un point commun entre 2 cartes quelconques

# %%
# un table de hash : card1, card2 -> symbole
common_symbol = {}

# on range les conflits par cardinal de l'intersection (0 ou 2)
for c1 in all_cards:
    for c2 in all_cards:
        # comme on est sûr que les deux boucles se font
        # dans le même ordre, on peut mettre break 
        # si on fait continue, on a deux fois trop de couples 
        if c1 is c2:
            break
        # combien de cartes en commun
        common = (c1 & c2)
        if len(common) != 1:
            print(f"--- between {c1} and {c2}: {common} common items:\n")
            print(common)
        else:
            common_symbol[c1, c2] = common.pop()


# %%
def find_common(c1, c2):
    return common_symbol.get( (c1, c2), common_symbol.get( (c2, c1), None))


# %%
c1, c2 = all_cards[:2]
print(f"entre\n{c1}\net\n{c2}\nil y a un seul point commun '{find_common(c1, c2)}'")

# %% [markdown]
# ### symboles les plus utilisés

# %%
from collections import defaultdict

# %% [markdown]
# `symbol_to_cards` : un hash (dictionnaire) qui associe à un symbole l'ensemble des cartes où il apparaît

# %%
symbol_to_cards = defaultdict(set)

for card in all_cards:
    for symbol in card:
        symbol_to_cards[symbol].add(card)


# %% [markdown]
# on le trie par fréquence d'apparition :

# %%
# le critère de tri: la taille de la partie droite du tuple
# et si égalité, alphanumérique sur la partie gauche du tuple

def symbol_cards_key(sc):
    symbol, cards = sc
    return len(cards), symbol

symbol_cards_list = list(symbol_to_cards.items())
symbol_cards_list.sort(key = symbol_cards_key)

# %%
# de nouveau on essaie d'afficher tout ça sur une page
# les cartes qui apparaissent le moins sont en premier

columns = 5
colwidth = 15

for i, (symbol, scards) in enumerate(symbol_cards_list):
    print(f"{symbol:>{colwidth}s} [{len(scards):2}] ", end="")
    if (i+1) % columns == 0:
        print()    

# %% [markdown]
# ## les cartes en fonction des symboles

# %% [markdown]
# Pour montrer la même information mais avec le détail des cartes.  
# Par exemple, on sait que `bonhommeneige` apparait sur 6 cartes mais maintenant on veut voir lesquelles:

# %%
cards = list(symbol_cards_list[0][1])[0].counter

# %%
# en vrac
if False:
    for symbol, cards in symbol_cards_list:
        print(f"{symbol:15s} ", end="")
        print(" - ".join(f"{card.counter:02}" for card in sorted(cards, key=lambda card: card.counter)))

# %% [markdown]
# ## nombre de fois qu'un symbole est un point commun

# %%
occurrences = defaultdict(int)

for c1 in all_cards:
    for c2 in all_cards:
        if c1 is c2:
            # si on mettait continue ici on n'aurait le bon nombre mais double
            break
        common = common_symbol[c1, c2]
        occurrences[common] += 1
        


# %%
# de nouveau on essaie d'afficher tout ça sur une page
# les cartes qui apparaissent le moins sont en premier 
# et les égalités par ordre alphabétique

def count_key(item):
    symbol, count = item
    return (count, symbol)

less_often_first = sorted(occurrences.items(), key=count_key)

columns = 5
colwidth = 15

for i, (symbol, occurrences) in enumerate(less_often_first):
    print(f"{symbol:>{colwidth}s} [{occurrences}] ", end="")
    if (i+1) % columns == 0:
        print()    

# %% [markdown]
# ## une petite vérification

# %%
# en tout on a un nombre de paires de cartes
total_pairs = N_CARDS * (N_CARDS-1) // 2

total_pairs

# %%
# qui doit correspondre avec la somme des occurrences de points communs 
# qu'on vient de calculer
sum(couple[1] for couple in less_often_first)

# %% [markdown]
# ## une remarque

# %% [markdown]
# C'est troublant tout de même que tous ces nombres d'occurrences font partie de la même suite:

# %%
# (1, 3, 6, 10,) 15, 21, 28
for n in range(1, 10):
    print(n*(n+1)//2)

# %% [markdown]
# ## dessiner autrement
#
# juste par curiosité, ça donne quelque chose si on dessine toutes les cartes en fonction des symboles qui sont dedans ?
#
# pour commencer on les met en vrac...

# %%
from itertools import count

# le rang du symbole dépend de l'ordre alphabétique
symbol_counter = dict(zip(sorted(symbols), count(1)))
list(symbol_counter.items())[:2]

# %%
# le tableau des X a n_cards * SYMBOLS_PER_CARD éléments
#X = [1, 1, ... Nx... , 2, 2, ... Nx, ..... N_CARDS, ... Nx]

X = []
for n in range(1, N_CARDS+1):
    X += SYMBOLS_PER_CARD*[n]

# dans l'ordre de all_cards, et comme valeur ce qu'on a calculé au dessus
# i.e. le rang du symbole dans l'ordre alphabétique
Y = [symbol_counter[symbol] for card in all_cards for symbol in card]


# %%
def show_map(X, Y, figsize=(8, 8)):
    plt.figure(figsize=figsize)
    plt.title(f"N={SYMBOLS_PER_CARD} X= {N_CARDS} cards, Y= {N_SYMBOLS} symbols")
    plt.scatter(X, Y, marker='.', c='red')
    plt.savefig(f"drawing-{SYMBOLS_PER_CARD:02}.svg")
    
show_map(X, Y)

# %% [markdown]
# ## pareil, mais dans un autre ordre

# %% [markdown]
# * on va prendre le symbole qui apparait le moins souvent
# * puis on va prendre les cartes dans lesquels il apparait; et ajouter les symboles
# * ce qui va donner des cartes ....

# %%
symbol0 = less_often_first[0][0]
print(f"{symbol0=}")

# %%
symbol0 = 'zebre'


# %%
def compute_x_y(symbol0):

    # we need an ordered set, so we use a dict with a True value
    symbols_foo = {symbol0: True}
    cards_foo = {}

    while (len(symbols_foo) < N_SYMBOLS) or (len(cards_foo) < N_CARDS):
        new_symbols = {}
        for symbol in symbols_foo.copy():
            for card in symbol_to_cards[symbol]:
                if card in cards_foo:
                    continue
                cards_foo[card] = True
                for symbol in card:
                    if symbol in symbols_foo:
                        continue
                    new_symbols[symbol] = True
#        for symbol in sorted(new_symbols, key=lambda s: len(symbol_to_cards[s])):
        for symbol in new_symbols:
            symbols_foo[symbol] = True

    X = []
    for n in range(1, N_CARDS+1):
        X += [n] * SYMBOLS_PER_CARD

    # the order in which the cards appear in X
    ordered_cards = list(cards_foo.keys())

    def swapx(n1, n2):
        # we pass indices that start at 1
        n1, n2 = n1-1, n2-1
        ordered_cards[n1], ordered_cards[n2] = ordered_cards[n2], ordered_cards[n1]
                
    # the order in which the symbols appear in Y
    symbol_counter = {symbol: counter for counter, symbol in enumerate(symbols_foo, 1)}

    def swapy(n1, n2):
        for k, v in symbol_counter.items():
            if v == n1:
                symbol_counter[k] = n2
            elif v == n2:
                symbol_counter[k] = n1

    
    Y = []
    for card in ordered_cards:
        for symbol in card:
            Y.append(symbol_counter[symbol])

    print(f"{len(X)=} and {len(Y)=}")
    
    return X, Y

X, Y = compute_x_y(symbol0)
show_map(X, Y, figsize=(9, 6))

# %%
symbol0 = 'bonhommedeneige'

# we need an ordered set, so we use a dict with a True value
symbols_foo = {symbol0: True}
cards_foo = {}

while (len(symbols_foo) < N_SYMBOLS) or (len(cards_foo) < N_CARDS):
    for symbol in symbols_foo.copy():
        for card in symbol_to_cards[symbol]:
            cards_foo[card] = True
            for symbol in card:
                symbols_foo[symbol] = True
                #print(f"added symbol {symbol}")

X = []
for n in range(1, N_CARDS+1):
    X += [n] * SYMBOLS_PER_CARD

symbol_counter = {symbol: counter for counter, symbol in enumerate(symbols_foo, 1)}


def swapy(n1, n2):
    for k, v in symbol_counter.items():
        if v == n1:
            symbol_counter[k] = n2
        elif v == n2:
            symbol_counter[k] = n1

def swapx(n1, n2):
    # we pass indices that start at 1
    n1, n2 = n1-1, n2-1
    ordered_cards[n1], ordered_cards[n2] = ordered_cards[n2], ordered_cards[n1]

# beware this is not commutative so the order here is important
swapy(9, 12)
swapy(16, 18)
swapy(23, 29)
swapy(10, 13)
swapy(19, 17)
swapy(24, 28)
swapy(15, 11)
swapy(14, 12)
swapy(15, 13)
swapy(14, 15)
swapy(19, 21)
swapy(25, 28)
swapy(26, 27)
swapy(29, 27)
swapy(31, 33)
swapy(32, 36)
swapy(33, 34)
swapy(34, 36)
swapy(38, 42)
swapy(39, 40)
swapy(40, 41)
swapy(41, 42)

ordered_cards = list(cards_foo.keys())

swapx(14, 17)
swapx(16, 20)
swapx(18, 19)
swapx(21, 22)
swapx(23, 27)
swapx(24, 27)
swapx(28, 30)
swapx(29, 32)
swapx(30, 32)
swapx(31, 32)
swapx(32, 33)
swapx(35, 36)
swapx(36, 41)
swapx(37, 39)
swapx(39, 41)
swapx(40, 41)
swapx(42, 48)
swapx(44, 47)
swapx(45, 47)
swapx(49, 53)
swapx(50, 51)
swapx(51, 52)
swapx(52, 54)
swapx(53, 55)
swapx(54, 55)

Y = []
for card in ordered_cards:
    for symbol in card:
        Y.append(symbol_counter[symbol])
        
print(f"{len(X)=} and {len(Y)=}")

show_map(X, Y, figsize=(9, 6))
