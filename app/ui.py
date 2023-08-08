import os

import helpers as h

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_int(prompt="> ", error="\"{raw}\" is not a valid integer", range=None):
    while True:
        raw = input(prompt).split(" ")[0]
        try:
            result = int(raw)
            if range:
                if result >= range[0] and result <= range[1]:
                    return result
                else:
                    print(f"\"{result}\" not in range {range[0]}-{range[1]}")
            else:
                return result
        except ValueError:
            print(error.replace("{raw}", raw))


def decks_ui(db):
    clear()
    decks = h.get_decks(db)
    print("Deck\t\tDescription\tDue")
    for i, deck in enumerate(decks):
        print(f"[{i+1}] {deck[0]}\t{deck[1]}\t{h.get_num_due(db, deck[0])}")
    inp = get_int(range=(1, len(decks)))
    if inp >= 0 and inp <= len(decks):
        deck_opts_ui(db, decks[inp-1][0])

def deck_opts_ui(db, deck_name):
    clear()
    print(f"Deck: {deck_name}")
    print("[1] Study\n[2] Add Card\n[3] Delete Card\n[4] Edit Card\n[5] Delete Deck\n[6] View Deck\n[7] Back")
    inp = get_int(range=(1, 7))
    match(inp):
        case(1):
            study_ui(db, deck_name)
        case(2):
            add_card_ui(db, deck_name)
        case(3):
            delete_card_ui(db, deck_name)
        case(4):
            edit_card_ui(db, deck_name)
        case(5):
            delete_deck_ui(db, deck_name)
        case(6):
            view_deck_ui(db, deck_name)
        case(7):
            return
        case(_):
            deck_opts_ui(db, deck_name)

def study_ui(db, deck_name):

    due_cards = h.get_due_cards(db, deck_name)
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
            choice = get_int(range=(1,3))
            match choice:
                case(1):
                    h.move_bin(db, deck_name, front, change=-1)
                case(2):
                    pass
                case(3):
                    h.move_bin(db, deck_name, front, change=1)
                    due_cards.pop(front)
                case(_):
                    pass
            h.update_due(db, deck_name, front)
            due_cards = h.get_due_cards(db, deck_name)
            num_left = len(due_cards)
    input("No more cards due. Press enter to continue")


                
        


def add_card_ui(db, deck_name):
    clear()

    front = None
    taken_fronts = h.get_deck(db, deck_name).keys()

    print(f"Adding Card to \"{deck_name}\"")
    print("Enter the text for the front of the card or \"exit\" to exit")
    while True:
        front = input("> ")
        if front == "exit": return
        if not front in taken_fronts:
            break
        print(f"\"{front}\" is already taken")

    print("Enter the text for the back of the card or \"exit\" to exit")
    back = input("> ")
    if back == "exit": return

    h.add_card(db, deck_name, front, back)
    


def delete_card_ui(db, deck_name):
    clear()

    taken_fronts = h.get_deck(db, deck_name).keys()

    print(f"Deleting Card From \"{deck_name}\"")
    print("Enter the text for the front of the card to delete or \"exit\" to exit")
    while True:
        front = input("> ")
        if front == "exit": return
        if front in taken_fronts:
            print(f"Are you sure you want to delete {front} from {deck_name}? [Y/n]")
            inp = input("> ")
            if inp[0] != "n" and inp != "N":
                h.delete_card(db, deck_name, front)
                return
            else:
                print(f"\"{front}\" was not deleted")
        else:
            print(f"\"{front}\" is not in this deck")


def edit_card_ui(db, deck_name):
    clear()

    taken_fronts = h.get_deck(db, deck_name).keys()

    print(f"Editing Card From \"{deck_name}\"")
    print("Enter the text for the front of the card to edit or \"exit\" to exit")
    while True:
        front = input("> ")
        if front == "exit": return
        if front in taken_fronts:
            print(f"Old Back: {h.get_back(db, deck_name, front)}")
            print(f"Enter the text for the back of the card or \"exit\" to exit")
            back = input("> ")
            if back == "exit": return
            h.edit_card(db, deck_name, front, back)
            return
        else:
            print(f"\"{front}\" is not in this deck")

def delete_deck_ui(db, deck_name):
    clear()

    print(f"Are you sure you want to delete {deck_name}? [Y/n]")
    inp = input("> ")
    if inp[0] != "n" and inp != "N":
        h.delete_deck(db, deck_name)

def view_deck_ui(db, deck_name):
    clear()
    print(f"Deck: {deck_name}")
    print("Front\tBack")
    for front, back in h.get_deck(db, deck_name).items():
        print(f"{front}\t{back}")
    input("Press enter to continue")


def repl(db):
    while True:
        decks_ui(db)