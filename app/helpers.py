def get_deck(connection, deck_name):
    cursor = connection.cursor()
    cursor.execute(f'SELECT front,back FROM cards WHERE deck="{deck_name}"')
    results = [{front: back} for (front, back) in cursor]
    cursor.close()
    return results