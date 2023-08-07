def get_deck(connection, deck_name):
    cursor = connection.cursor()
    cursor.execute(f'SELECT front,back FROM cards WHERE deck="{deck_name}"')
    results = [{front: back} for (front, back) in cursor]
    cursor.close()
    return results

def get_decks(connection):
    cursor = connection.cursor()
    cursor.execute(f'SELECT `name` FROM decks')
    results = [deck[0] for deck in cursor]
    cursor.close()
    return results

def get_card(connection, deck_name, card_front):
    cursor = connection.cursor()
    cursor.execute(f'SELECT front,back FROM cards WHERE deck="{deck_name}" AND front="{card_front}"')
    results = [{front: back} for (front, back) in cursor]
    cursor.close()
    return results

def get_all_cards(connection):
    cursor = connection.cursor()
    cursor.execute(f'SELECT front,back FROM cards')
    results = [{front: back} for (front, back) in cursor]
    cursor.close()
    return results

def add_card(connection, deck_name, card_front, card_back):
    cursor = connection.cursor()
    cursor.execute(f'INSERT INTO cards (deck, front, back) VALUES ("{deck_name}", "{card_front}", "{card_back}")')
    connection.commit()
    cursor.close()
    return

def delete_card(connection, deck_name, card_front):
    cursor = connection.cursor()
    cursor.execute(f'DELETE FROM cards WHERE deck="{deck_name}" AND front="{card_front}"')
    connection.commit()
    cursor.close()
