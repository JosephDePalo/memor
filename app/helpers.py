""" helper functions for interacting with the database """

DATE_UPDATES = { # In days
    0: 0,
    1: 1,
    2: 3,
    3: 5,
    4: 10,
    5: 20
}

def sql_commit(connection, query):
    """ Executes the given query and commits the changes."""
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()

def sql_get_list(connection, query):
    """ Executes the given query and returns the results as a list. """
    cursor = connection.cursor()
    cursor.execute(query)
    result = list(cursor)
    cursor.close()
    return result


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
    return sql_get_list(connection, 'SELECT `name`,`desc` FROM decks')

def get_back(connection, deck_name, card_front):
    """ Returns the back of the given card. """
    return sql_get_list(connection,
                        f'SELECT back FROM cards\
                         WHERE deck="{deck_name}" AND front="{card_front}"')[0][0]

def add_card(connection, deck_name, card_front, card_back):
    """ Adds a card to the given deck. """
    sql_commit(connection,
               f'INSERT INTO cards (deck, front, back)\
                VALUES ("{deck_name}", "{card_front}", "{card_back}")')

def delete_card(connection, deck_name, card_front):
    """ Deletes a card from the given deck. """
    sql_commit(connection,
               f'DELETE FROM cards\
                WHERE deck="{deck_name}" AND front="{card_front}"')

def edit_card(connection, deck_name, card_front, card_back):
    """ Edits a card in the given deck. """
    sql_commit(connection,
               f'UPDATE cards SET back="{card_back}"\
                WHERE deck="{deck_name}" AND front="{card_front}"')


def get_num_due(connection, deck_name):
    """ Returns the number of cards due in the given deck. """
    return sql_get_list(connection,
                        f'SELECT COUNT(*) FROM cards\
                        WHERE deck="{deck_name}" AND due <= NOW()')[0][0]

def get_due_cards(connection, deck_name):
    """ Returns a dictionary of cards due in the given deck. """
    cursor = connection.cursor()
    cursor.execute(f'SELECT front,back FROM cards WHERE deck="{deck_name}" AND due <= NOW()')
    result = dict(cursor)
    cursor.close()
    return result

def get_deck_size(connection, deck_name):
    """ Returns the number of cards in the given deck. """
    return sql_get_list(connection,
                        f'SELECT COUNT(*) FROM cards WHERE deck="{deck_name}"')[0][0]

def delete_deck(connection, deck_name):
    """ Deletes the given deck. """
    sql_commit(connection,
               f'DELETE FROM cards WHERE deck="{deck_name}"')
    sql_commit(connection,
               f'DELETE FROM decks WHERE name="{deck_name}"')

def create_deck(connection, deck_name):
    """ Creates a new deck with the given name. """
    sql_commit(connection,
               f'INSERT INTO decks (name) VALUES ("{deck_name}")')

def move_bin(connection, deck_name, front, change=1):
    """ Moves the given card's bin up or down by the given amount. """
    cursor = connection.cursor()
    cursor.execute(f'SELECT bin FROM cards WHERE deck="{deck_name}" AND front="{front}"')
    card_bin = [bin[0] for bin in cursor][0]
    if card_bin + change < 0 or card_bin + change > 5:
        return
    cursor.execute(f'UPDATE cards SET bin=bin+{change}\
                   WHERE deck="{deck_name}" AND front="{front}"')
    connection.commit()
    cursor.close()

def update_due(connection, deck_name, front):
    """ Updates the due date of the given card. """
    cursor = connection.cursor()
    cursor.execute(f'SELECT bin FROM cards WHERE deck="{deck_name}" AND front="{front}"')
    card_bin = [bin[0] for bin in cursor][0]
    cursor.execute(f'UPDATE cards SET due=DATE_ADD(NOW(), INTERVAL {DATE_UPDATES[card_bin]} DAY)\
                   WHERE deck="{deck_name}" AND front="{front}"')
    connection.commit()
    cursor.close()
