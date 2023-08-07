import os

import helpers as h

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def decks_ui(db):
    clear()
    decks = h.get_decks(db)
    print("Deck\t\tDescription\tDue")
    for i, deck in enumerate(decks):
        print(f"[{i+1}] {deck[0]}\t{deck[1]}\t{h.get_num_due(db, deck[0])}")
    inp = input("> ").split(" ")[0]
    if inp >= 0 and inp <= len(decks):
        deck_opts_ui(db, decks[inp-1][0])

def deck_opts_ui(db, deck_name):
    clear()
    print(f"Deck: {deck_name}")
    print("[1] Study\n[2] Add Card\n[3] Delete Card\n[4] Edit Card\n[5] Delete Deck\n[6] View Deck\n[7] Back")
    inp = input("> ").split(" ")[0]
    match(inp):
        case("1"):
            study_ui(db, deck_name)
        case("2"):
            add_card_ui(db, deck_name)
        case("3"):
            delete_card_ui(db, deck_name)
        case("4"):
            edit_card_ui(db, deck_name)
        case("5"):
            delete_deck_ui(db, deck_name)
        case("6"):
            view_deck_ui(db, deck_name)
        case("7"):
            decks_ui(db)
        case(_):
            deck_opts_ui(db, deck_name)

def study_ui(db, deck_name):
    pass

def add_card_ui(db, deck_name):
    pass

def delete_card_ui(db, deck_name):
    pass

def edit_card_ui(db, deck_name):
    pass

def delete_deck_ui(db, deck_name):
    pass

def view_deck_ui(db, deck_name):
    pass


def repl(db):
    while True:
        decks_ui(db)