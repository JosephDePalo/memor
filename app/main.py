import time

import mysql.connector

from ui import repl

DB_CONFIG = {
            'user': 'root',
            'password': 'root',
            'host': 'db',
            'port': '3306',
            'database': 'flashcards'
            }

def connect_db(config, num_tries=10):
    """
    Connects to the MYSQL database using the given config.
    Returns None if unable to connect.
    """
    for conn_tries in range(num_tries):
        try:
            connection = mysql.connector.connect(**config)
            break
        except mysql.connector.Error as err:
            if conn_tries == num_tries - 1:
                print(f"Failed to connect to database: {err}")
                return None
            time.sleep(1)
    return connection

def main():
    """ Main function. """
    conn = connect_db(DB_CONFIG)
    if conn is None:
        return
    repl(conn)
    conn.close()

if __name__ == '__main__':
    main()
