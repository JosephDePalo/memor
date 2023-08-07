import mysql.connector
import time

import helpers as h

connection = None
for conn_tries in range(0, 10):
    try:
        config = {
            'user': 'root',
            'password': 'root',
            'host': 'db',
            'port': '3306',
            'database': 'flashcards'
        }
        connection = mysql.connector.connect(**config)
        break
    except:
        if conn_tries == 9:
            print('Failed to connect to database')
            exit(1)
        else:
            time.sleep(1)

print(h.get_deck(connection, 'italian'))
connection.close()


