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
# !head -8 cards08.txt

# %% [markdown]
# ## les classes

# %%
SHOW_FREQUENCIES = False

# un symbole est représenté par une chaine
# et un compte d'occurrences
class Symbol:
    """
    chcun des symboles dessinés sur les cartes
    """
    def __init__(self, string):
        self.string = string
        self.frequency = 0
        self.cards = set()
        self.X = -1

    def __repr__(self):
        text = f"{self.string}"
        if SHOW_FREQUENCIES and self.frequency != 0:
            text += f" ({self.frequency})"
        return text
    def __format__(self, spec):
        return format(self.__repr__(), spec)

    def __lt__(self, other):
        return (self.frequency, self.string) < (other.frequency, other.string)
    
    def seen_on_card(self, card):
        self.cards.add(card)
        self.frequency += 1


# %%
# une carte est un ensemble de symboles
class Card(set):
    """
    le modèle pour chaque carte du jeu
    """
    
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        # the sum of frequencies
        self.frequency = 0
        self.Y = -1
        
    def compute_frequency(self):
        self.frequency = sum(symbol.frequency for symbol in self)
        
    def _contents(self):
        return " ".join(sorted(s.string for s in self))
    def __repr__(self):
        text = set.__repr__(self) 
        if SHOW_FREQUENCIES:
            text += f" ({self.frequency:2d})" 
        return text
    def __hash__(self):
        return hash(self._contents)
    def __eq__(self, other):
        return self._contents() == other._contents()


# %%
def read_cards(filename):
    """
    returns
    SYMBOLS as a ordered list of Symbols
    CARDS as an ordered list of Cards 
#    sorted by frequency (card freq = sum of symbols freqs)
    """
    symbols_dict = {}
    cards = []
    symbols_per_card = None
    with open(filename) as f:
        for line in f:
            if '#' in line:
                continue
            line_symbols = []
            for x in line.split():
                if x not in symbols_dict:
                    symbol = symbols_dict[x] = Symbol(x)
                else:
                    symbol = symbols_dict[x]
                if symbol in line_symbols:
                    print(f"ignoring duplicate {symbol}")
                else:
                    line_symbols.append(symbol)
            if symbols_per_card is None:
                symbols_per_card = len(line_symbols)
            card = Card(line_symbols)
            if len(card) != symbols_per_card:
                print(f"ignoring incomplete card with {len(card)} items {card}")
                continue
            cards.append(card)
            for symbol in line_symbols:
                symbol.seen_on_card(card)
    for card in cards:
        card.compute_frequency()
    # on les trie dans cet ordre
    cards.sort(key = lambda card: card.frequency)
#    symbols = sorted(symbols_dict.values())
    symbols = list(symbols_dict.values())
    return symbols_per_card, cards, symbols


# %% [markdown]
# ## construction du paquet de cartes

# %%
FILENAME = "cards05.txt"

# computed later on
N_SYMBOLS = 0

# %%
# will be updated by read_cards based on the first card
N = SYMBOLS_PER_CARD = 0
# and this will be filled too
SYMBOLS = []
CARDS = []

SYMBOLS_PER_CARD, CARDS, SYMBOLS = read_cards(FILENAME)

# a shortcut
N = SYMBOLS_PER_CARD

EXPECTED = N * (N-1) + 1

# %%
N_CARDS, N_SYMBOLS = len(CARDS), len(SYMBOLS)
print(f"with {SYMBOLS_PER_CARD} symbols per card, we have {N_CARDS} cards and {N_SYMBOLS} symbols")

# %%
# la liste des symboles, un peu mise en forme
COLWIDTH = max(len(symbol.string) for symbol in SYMBOLS)
COLUMNS = 70 // (COLWIDTH + 6)

for i, symbol in enumerate(sorted(SYMBOLS)):
    print(f"{symbol:>{COLWIDTH}s} [{symbol.frequency:2}] ", end="")
    ((i+1) % COLUMNS == 0) and print()

# %% [markdown]
# ## vérifications

# %%
# le nombre de cartes et de symboles
print(f"CARDS: {len(CARDS)==EXPECTED} "
      f"and SYMBOLS: {len(SYMBOLS)==EXPECTED}")

# %% [markdown]
# ### toutes les cartes ont le bon nombre de symboles

# %%
for card in CARDS:
    if len(card) != SYMBOLS_PER_CARD:
        print(f"OOPS {card} -> {len(card)}")

# %% [markdown]
# ### exactement un point commun entre 2 cartes quelconques

# %%
# un table de hash : card1, card2 -> symbole
common_symbol = {}

# on range les conflits par cardinal de l'intersection (0 ou 2)
for c1 in CARDS:
    for c2 in CARDS:
        # comme on est sûr que les deux boucles se font
        # dans le même ordre, on peut mettre break 
        # si on fait continue, on a deux fois trop de couples 
        if c1 is c2:
            continue
        # combien de cartes en commun
        common = (c1 & c2)
        if len(common) != 1:
            print(f"OOPS between {c1} and {c2}: {len(common)} common items:\n")
            print(common)
        else:
            common_symbol[c1, c2] = common.pop()
            
print(f"expected {len(CARDS) * (len(CARDS)-1)} and got {len(common_symbol)}")


# %%
def find_common(c1, c2):
    return next(iter(c1&c2))


# %% [markdown]
# ### peut-on ajouter des cartes ?

# %%
from itertools import combinations

def missing_cards_avoiding(avoid=None):

    avoid = [] if avoid is None else avoid

    solutions = []
    against = CARDS[:]
    first_hit = None

    for pick in combinations(SYMBOLS, SYMBOLS_PER_CARD):
        card = Card(pick)
        if card in CARDS:
            continue
        if card in avoid:
            continue
        for other in against:
            if len(card & other) != 1:
                break
        else:
            # display in order
#            print(" ".join(sorted(symbol.string for symbol in card)))
            against.append(card)
            solutions.append(card)
            if first_hit is None:
                first_hit = card
                print(f"{first_hit=}")
    if len(solutions) + len(CARDS) == EXPECTED:
        print("BINGO")
        return solutions

    else:
        print(f"NOPE with {first_hit=} (avoiding {len(avoid)} cards)")
        print(f"got {len(solutions)} solutions, "
              f" was expecting {EXPECTED-len(solutions)}")
        return first_hit
        
def missing_cards():
    avoid = []
    while True:
        result = missing_cards_avoiding(avoid)
        if isinstance(result, list):
            print("BINGO")
            for card in result:
                print(card)
            return result
        else:
            print(f"trying again without {result}")
            avoid.append(result)
            
            
if len(CARDS) == EXPECTED:
    print("you're all set")
else:
    solutions = missing_cards()


# %% [markdown]
# ### pour ajouter une carte partiellement faite à la main

# %%
def complete_card(*partial_items):
    partial_symbols = {
        s for item in partial_items for s in SYMBOLS if str(item) == s.string
    }
    new_card = Card(partial_symbols)
    # the starting cards:
    # the N first cards, that remain
    # i.e. that do not contain the partial items
    remaining_cards = [
        card for card in CARDS if not (card & new_card)
    ]
    print("1", len(remaining_cards))
    for c in remaining_cards:
        print(c)
    # the first ref card
    for s in remaining_cards[0]:
        # assuming we take that one
        new_card.add(s)
        remaining_cards = [
            card for card in remaining_cards if not (card & new_card)
        ]
        break
    print("2", len(remaining_cards))
    for c in remaining_cards:
        print(c)
    return remaining_cards

#complete_card(4, 7, 15);

    

# %% [markdown]
# ## nombre de fois qu'un symbole est un point commun

# %%
from collections import defaultdict

MATCHES = defaultdict(int)

for c1 in CARDS:
    for c2 in CARDS:
        if c1 is c2:
            # si on mettait continue ici on aurait le bon nombre mais double
            break
        common = find_common(c1, c2)
        if not common:
            pass #print(f"s.t. wrong with {c1} x {c2}")
        MATCHES[common] += 1
        
len(MATCHES) == EXPECTED

# %%
# dans un graphe 'propre' on devrait avoir toutes les valeurs égales à ceci
EXPECTED2 = (N-1) * (N-2)
set(MATCHES.values()) == {EXPECTED2}


# %%
# de nouveau on essaie d'afficher tout ça sur une page
# les cartes qui apparaissent le moins sont en premier 
# et les égalités par ordre alphabétique

def count_key(item):
    symbol, count = item
    return (count, symbol)

def show_matches_count():
    less_often_first = sorted(MATCHES.items(), key=count_key)

    columns = 4
    colwidth = 10

    for i, (symbol, count) in enumerate(less_often_first):
        print(f"{symbol:>{colwidth}s} [{count}] ", end="")
        if (i+1) % columns == 0:
            print()

show_matches_count()            

# %% [markdown]
# ## une petite vérification

# %%
# en tout on a un nombre de paires de cartes
total_pairs = N_CARDS * (N_CARDS-1) // 2

total_pairs

# %%
# qui doit correspondre avec la somme des occurrences de points communs 
# qu'on vient de calculer
sum(MATCHES.values())

# %% [markdown]
# ## une remarque

# %% [markdown]
# C'est troublant tout de même que tous ces nombres d'occurrences font partie de la même suite:

# %%
# (1, 3, 6, 10,) 15, 21, 28
for n in range(1, 10):
    print(n*(n+1)//2)


# %%
# CARDS

# %%
# SYMBOLS

# %% [markdown]
# ## dessiner
#
# on met un point pour chaque symbole sur une carte

# %%
def x(n):
    return n
def xs(L):
    return [x(_) for _ in L]
def y(n):
    return EXPECTED-n
def ys(L):
    return [y(_) for _ in L]

def show_map(figsize=(8, 8)):

    y_labels = sorted(SYMBOLS, key=lambda s: s.X)
    
    X, Y, colors = [], [], []
    for card in CARDS:
        for symbol in card:
            X.append(x(symbol.X))
            Y.append(y(card.Y))
            colors.append(color(card.Y, symbol.X))
    
    fig, ax = plt.subplots(figsize=figsize)
    plt.title(f"N={SYMBOLS_PER_CARD} X={N_CARDS} cards, Y={N_SYMBOLS} symbols")
    if y_labels:
        ax.set_yticklabels(y_labels)
        ax.set_yticks(ys(range(N_SYMBOLS)))
        ax.tick_params(axis='both', which='major', labelsize=8)
        ax.tick_params(axis='both', which='minor', labelsize=6)
    
    plt.scatter(X, Y, marker='o', c=colors)
    # la grille
    for i in range(1, N):
        step = 1+i*(N-1)-0.5
        plt.plot(xs([-0.5, EXPECTED-0.5]), 
                 ys([step, step]), 
                 'k-', linewidth=0.5)
        plt.plot(xs([step, step]),
                 ys([-0.5, EXPECTED-0.5]),
                 'k-', linewidth=0.5)
    plt.savefig(f"drawing-{SYMBOLS_PER_CARD:02}.svg")
    plt.savefig(f"drawing-{SYMBOLS_PER_CARD:02}.png")    


# %%
def is_in(n, card):
    for s in card:
        if s.string == str(n):
            return True

# need to be extended if n > 6

COLORS = ['blue', 'green', 'pink', 'lightblue', 'red', 'orange']
def color(x, y, verbose=False):
    qx = (x-1)//(N-1)
    qy = (y-1)//(N-1)
    rx, ry = (x-1)%(N-1), (y-1)%(N-1)
    if (qx <= 0) or (qy <= 0):
        return COLORS[0]
    elif (qx == 1) or (qy == 1):
        return COLORS[1]
    else:
        verbose and print(f"{x=} {rx=}")
        first_line = x - rx
        card = CARDS[first_line]
        # what is the offset on that line
        first_column = y - ry + 1
        verbose and print(f"{first_column=}, {first_line=}", card)
        for i in range(N-1):
            verbose and print("trying", first_column + i)
            if is_in(first_column + i, card):
                verbose and print(f"bingo {i=}")
                return COLORS[2+(i-1)]
        return 'black'


# %% [markdown]
# pour les jeux synthétisés, c'est facile

# %%
for index, card in enumerate(CARDS):
    card.Y = index
for index, symbol in enumerate(SYMBOLS):
    symbol.X = index

# %%
show_map()

# %% [markdown]
# ## dessiner tout ça
#
# pour les jeux reportés de dobble, le truc c'est de trouver le bon ordre à la fois pour les cartes et pour les symboles

# %% [markdown]
# * on va prendre le symbole qui apparait le moins souvent
# * puis on va prendre les cartes dans lesquels il apparait; et ajouter les symboles
# * ce qui va donner des cartes ....

# %%
symbol0 = SYMBOLS[0]
symbol0


# %%
def compute_x_y(symbol0):

    # we need an ordered set, so we use a dict with a True value
    symbols_dictset = {symbol0: True}
    cards_dictset = {}

    while (len(symbols_dictset) < N_SYMBOLS) or (len(cards_dictset) < N_CARDS):
        new_symbols = {}
        for symbol in symbols_dictset.copy():
            for card in symbol.cards:
                if card in cards_dictset:
                    continue
                cards_dictset[card] = True
                for symbol in card:
                    if symbol in symbols_dictset:
                        continue
                    new_symbols[symbol] = True
        for symbol in new_symbols:
            symbols_dictset[symbol] = True
            
    # the order in which the cards appear in X
    for index, card in enumerate(cards_dictset.keys()):
        card.Y = index
    # the order in which the symbols appear in Y
    for index, symbol in enumerate(symbols_dictset):
        symbol.X = index

    # smallest occurence is equal to the number of vertical bars on the left
    S = symbol0.frequency
    # the cards corresponding to the vertical bars
#    vertical_cards = 0 # ordered_cards[1:S]
    # the first X-range (corresponding to symbol1)
    x_beg = symbol0.frequency+1
    x_end = x_beg + SYMBOLS[1].frequency
#    for card in vertical_cards[:1]:
#        pass
        

#compute_x_y(symbol0)
#show_map(figsize=(9, 6))

# %% [markdown]
# ***
