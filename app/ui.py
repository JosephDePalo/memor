import os

import helpers as h

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_decks(db):
    decks = h.get_decks(db)
    for i, deck in enumerate(decks):
        print(f"[{i+1}] {deck[0]}\t{deck[1]}")


def repl(db):
    while True:
        clear()
        show_decks(db)
        inp = input("> ")