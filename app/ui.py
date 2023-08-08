""" UI and primary logic for Memor """
import os

import helpers as h

def clear():
    """ Clears the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_int(prompt="> ", error="\"{raw}\" is not a valid integer", rng=None):
    """
    Gets an integer from the user and returns it. If the user enters "exit",
    returns -1. If the user enters a non-integer, prints error and tries again.
    If rng is specified, the integer must be in the range.
    """
    while True:
        raw = input(prompt).split(" ")[0]
        if raw == "exit":
            return -1
        try:
            result = int(raw)
            if rng:
                if result in range(rng[0], rng[1]+1):
                    return result
                print(f"\"{result}\" not in rng {rng[0]}-{rng[1]}")
            else:
                return result
        except ValueError:
            print(error.replace("{raw}", raw))


def decks_ui(connection):
    """
    Displays the decks and their descriptions. Returns -1 if the user wants to
    exit, otherwise returns 0.
    """
    clear()
    decks = h.get_decks(connection)
    print("Deck\t\tDescription\tDue")
    for i, deck in enumerate(decks):
        print(f"[{i+1}] {deck[0]}\t{deck[1]}\t{h.get_num_due(connection, deck[0])}")
    inp = get_int(rng=(1, len(decks)))
    if inp == -1:
        return -1
    deck_opts_ui(connection, decks[inp-1][0])
    return 0

def deck_opts_ui(connection, deck_name):
    """ Displays the options for a deck. """
    clear()
    print(f"Deck: {deck_name}")
    print("[1] Study\n[2] Add Card\n[3] Delete Card\n\
          [4] Edit Card\n[5] Delete Deck\n[6] View Deck\n[7] Back")
    inp = get_int(rng=(1, 7))
    match(inp):
        case(1):
            study_ui(connection, deck_name)
        case(2):
            add_card_ui(connection, deck_name)
        case(3):
            delete_card_ui(connection, deck_name)
        case(4):
            edit_card_ui(connection, deck_name)
        case(5):
            delete_deck_ui(connection, deck_name)
        case(6):
            view_deck_ui(connection, deck_name)
        case(7):
            return
        case(_):
            deck_opts_ui(connection, deck_name)

def study_ui(connection, deck_name):
    """
    Displays the cards in a deck and allows the user to review them. Based
    on how the user performs, each card's bin and due date are updated.
    """

    due_cards = h.get_due_cards(connection, deck_name)
    num_left = len(due_cards)
    while due_cards:
        for front in due_cards.copy():
            clear()
            print(f"Deck: {deck_name}\tRemaining: {num_left}")
            print(f"\t   {front}")
            input("Press enter to reveal the back")
            clear()
            print(f"Deck: {deck_name}\tRemaining: {num_left}")
            print(f"\t   {due_cards[front]}")
            print("[1] Fail  [2] OK  [3] Easy")
            choice = get_int(rng=(1,3))
            match choice:
                case(1):
                    h.move_bin(connection, deck_name, front, change=-1)
                case(2):
                    pass
                case(3):
                    h.move_bin(connection, deck_name, front, change=1)
                    due_cards.pop(front)
                case(_):
                    pass
            h.update_due(connection, deck_name, front)
            due_cards = h.get_due_cards(connection, deck_name)
            num_left = len(due_cards)
    input("No more cards due. Press enter to continue")

def add_card_ui(connection, deck_name):
    """ Adds a card to a deck."""
    clear()

    front = None
    taken_fronts = h.get_deck(connection, deck_name).keys()

    print(f"Adding Card to \"{deck_name}\"")
    print("Enter the text for the front of the card or \"exit\" to exit")
    while True:
        front = input("> ")
        if front == "exit":
            return
        if not front in taken_fronts:
            break
        print(f"\"{front}\" is already taken")

    print("Enter the text for the back of the card or \"exit\" to exit")
    back = input("> ")
    if back == "exit":
        return

    h.add_card(connection, deck_name, front, back)

def delete_card_ui(connection, deck_name):
    """ Deletes a card from a deck."""
    clear()

    taken_fronts = h.get_deck(connection, deck_name).keys()

    print(f"Deleting Card From \"{deck_name}\"")
    print("Enter the text for the front of the card to delete or \"exit\" to exit")
    while True:
        front = input("> ")
        if front == "exit":
            return
        if front in taken_fronts:
            print(f"Are you sure you want to delete {front} from {deck_name}? [Y/n]")
            inp = input("> ")
            if inp[0] != "n" and inp != "N":
                h.delete_card(connection, deck_name, front)
                return
            else:
                print(f"\"{front}\" was not deleted")
        else:
            print(f"\"{front}\" is not in this deck")


def edit_card_ui(connection, deck_name):
    """ Edits a card in a deck. """
    clear()

    taken_fronts = h.get_deck(connection, deck_name).keys()

    print(f"Editing Card From \"{deck_name}\"")
    print("Enter the text for the front of the card to edit or \"exit\" to exit")
    while True:
        front = input("> ")
        if front == "exit":
            return
        if front in taken_fronts:
            print(f"Old Back: {h.get_back(connection, deck_name, front)}")
            print("Enter the text for the back of the card or \"exit\" to exit")
            back = input("> ")
            if back == "exit":
                return
            h.edit_card(connection, deck_name, front, back)
            return
        else:
            print(f"\"{front}\" is not in this deck")

def delete_deck_ui(connection, deck_name):
    """ Deletes a deck. """
    clear()

    print(f"Are you sure you want to delete {deck_name}? [Y/n]")
    inp = input("> ")
    if inp[0] != "n" and inp != "N":
        h.delete_deck(connection, deck_name)

def view_deck_ui(connection, deck_name):
    """ Displays the cards in a deck. """
    clear()

    deck = h.get_deck(connection, deck_name)
    print(f"Deck: {deck_name}")
    print("Front\t\tBack\t\tBin\tDue")
    for front in deck:
        print(f"{front:16}{deck[front]['back']:16}{deck[front]['bin']}\t{deck[front]['due']}")
    input("Press enter to continue")


def repl(connection):
    """ The main REPL loop."""
    while True:
        ret_code = decks_ui(connection)
        if ret_code == -1:
            break
