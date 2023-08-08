
DATE_UPDATES = { # In days
    0: 0,
    1: 1,
    2: 3,
    3: 5,
    4: 10,
    5: 20
}


def get_deck(connection, deck_name):
    """
    Returns a dictionary of cards in the given deck. The keys are the fronts
    and the values are a dictionary containing the back, bin, and due date of
    each card.
    """
    cursor = connection.cursor()
    cursor.execute(f'SELECT front,back,bin,due FROM cards WHERE deck="{deck_name}"')
    results = {front: {"back":back, "bin":bin, "due":due} for (front, back, bin, due) in cursor}
    cursor.close()
    return results

def get_decks(connection):
    """ Returns a list of all decks and their descriptions. """
    cursor = connection.cursor()
    cursor.execute('SELECT `name`,`desc` FROM decks')
    results = [(name, desc) for (name, desc) in cursor]
    cursor.close()
    return results

def get_back(connection, deck_name, card_front):
    """ Returns the back of the given card. """
    cursor = connection.cursor()
    cursor.execute(f'SELECT back FROM cards WHERE deck="{deck_name}" AND front="{card_front}"')
    results = [back[0] for back in cursor]
    cursor.close()
    return results[0]

def add_card(connection, deck_name, card_front, card_back):
    """ Adds a card to the given deck. """
    cursor = connection.cursor()
    cursor.execute(f'INSERT INTO cards (deck, front, back) VALUES ("{deck_name}", "{card_front}", "{card_back}")')
    connection.commit()
    cursor.close()

def delete_card(connection, deck_name, card_front):
    """ Deletes a card from the given deck. """
    cursor = connection.cursor()
    cursor.execute(f'DELETE FROM cards WHERE deck="{deck_name}" AND front="{card_front}"')
    connection.commit()
    cursor.close()

def edit_card(connection, deck_name, card_front, card_back):
    """ Edits a card in the given deck. """
    cursor = connection.cursor()
    cursor.execute(f'UPDATE cards SET back="{card_back}" WHERE deck="{deck_name}" AND front="{card_front}"')
    connection.commit()
    cursor.close()


def get_num_due(connection, deck_name):
    """ Returns the number of cards due in the given deck. """
    cursor = connection.cursor()
    cursor.execute(f'SELECT COUNT(*) FROM cards WHERE deck="{deck_name}" AND due <= NOW()')
    result = list(cursor)[0][0]
    cursor.close()
    return result

def get_due_cards(connection, deck_name):
    """ Returns a dictionary of cards due in the given deck. """
    cursor = connection.cursor()
    cursor.execute(f'SELECT front,back FROM cards WHERE deck="{deck_name}" AND due <= NOW()')
    result = dict(cursor)
    cursor.close()
    return result

def get_deck_size(connection, deck_name):
    """ Returns the number of cards in the given deck. """
    cursor = connection.cursor()
    cursor.execute(f'SELECT COUNT(*) FROM cards WHERE deck="{deck_name}"')
    result = list(cursor)
    cursor.close()
    return result[0][0]

def delete_deck(connection, deck_name):
    """ Deletes the given deck. """
    cursor = connection.cursor()
    cursor.execute(f'DELETE FROM cards WHERE deck="{deck_name}"')
    cursor.execute(f'DELETE FROM decks WHERE name="{deck_name}"')
    connection.commit()
    cursor.close()

def create_deck(connection, deck_name):
    """ Creates a new deck with the given name. """
    cursor = connection.cursor()
    cursor.execute(f'INSERT INTO decks (name) VALUES ("{deck_name}")')
    connection.commit()
    cursor.close()
       
def move_bin(connection, deck_name, front, change=1):
    """ Moves the given card's bin up or down by the given amount. """
    cursor = connection.cursor()
    cursor.execute(f'SELECT bin FROM cards WHERE deck="{deck_name}" AND front="{front}"')
    card_bin = [bin[0] for bin in cursor][0]
    if card_bin + change < 0 or card_bin + change > 5:
        return
    cursor.execute(f'UPDATE cards SET bin=bin+{change} WHERE deck="{deck_name}" AND front="{front}"')
    connection.commit()
    cursor.close()

def update_due(connection, deck_name, front):
    """ Updates the due date of the given card. """
    cursor = connection.cursor()
    cursor.execute(f'SELECT bin FROM cards WHERE deck="{deck_name}" AND front="{front}"')
    card_bin = [bin[0] for bin in cursor][0]
    cursor.execute(f'UPDATE cards SET due=DATE_ADD(NOW(), INTERVAL {DATE_UPDATES[card_bin]} DAY) WHERE deck="{deck_name}" AND front="{front}"')
    connection.commit()
    cursor.close()
