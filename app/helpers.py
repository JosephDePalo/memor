def get_deck(connection, deck_name):
    cursor = connection.cursor()
    cursor.execute(f'SELECT front,back FROM cards WHERE deck="{deck_name}"')
    results = {front: back for (front, back) in cursor}
    cursor.close()
    return results

def get_decks(connection):
    cursor = connection.cursor()
    cursor.execute(f'SELECT `name`,`desc` FROM decks')
    results = [(name, desc) for (name, desc) in cursor]
    cursor.close()
    return results

def get_back(connection, deck_name, card_front):
    cursor = connection.cursor()
    cursor.execute(f'SELECT back FROM cards WHERE deck="{deck_name}" AND front="{card_front}"')
    results = [back[0] for back in cursor]
    cursor.close()
    return results[0]

def get_all_cards(connection):
    cursor = connection.cursor()
    cursor.execute(f'SELECT front,back FROM cards')
    results = {front: back for (front, back) in cursor}
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

def edit_card(connection, deck_name, card_front, card_back):
    cursor = connection.cursor()
    cursor.execute(f'UPDATE cards SET back="{card_back}" WHERE deck="{deck_name}" AND front="{card_front}"')
    connection.commit()
    cursor.close()


def get_num_due(connection, deck_name):
    cursor = connection.cursor()
    cursor.execute(f'SELECT COUNT(*) FROM cards WHERE deck="{deck_name}" AND due <= NOW()')
    results = [count for (count) in cursor]
    cursor.close()
    return results[0][0]

def get_due_cards(connection, deck_name):
    cursor = connection.cursor()
    cursor.execute(f'SELECT front,back FROM cards WHERE deck="{deck_name}" AND due <= NOW()')
    results = {front: back for (front, back) in cursor}
    cursor.close()
    return results

def get_deck_size(connection, deck_name):
    cursor = connection.cursor()
    cursor.execute(f'SELECT COUNT(*) FROM cards WHERE deck="{deck_name}"')
    results = [count for (count) in cursor]
    cursor.close()
    return results[0][0]

def delete_deck(connection, deck_name):
    cursor = connection.cursor()
    cursor.execute(f'DELETE FROM cards WHERE deck="{deck_name}"')
    cursor.execute(f'DELETE FROM decks WHERE name="{deck_name}"')
    connection.commit()
    cursor.close()

def create_deck(connection, deck_name):
    cursor = connection.cursor()
    cursor.execute(f'INSERT INTO decks (name) VALUES ("{deck_name}")')
    connection.commit()
    cursor.close()
    
def move_bin(connection, deck_name, front, change=1):
    cursor = connection.cursor()
    cursor.execute(f'SELECT bin FROM cards WHERE deck="{deck_name}" AND front="{front}"')
    card_bin = [bin[0] for bin in cursor][0]
    if card_bin + change < 0 or card_bin + change > 5:
        return
    cursor.execute(f'UPDATE cards SET bin=bin+{change} WHERE deck="{deck_name}" AND front="{front}"')
    connection.commit()
    cursor.close()
