import mysql.connector
import time

from ui import repl

db_config = {
            'user': 'root',
            'password': 'root',
            'host': 'db',
            'port': '3306',
            'database': 'flashcards'
            }

def connect_db(config, num_tries=10):
    for conn_tries in range(0, num_tries):
        try:
            connection = mysql.connector.connect(**config)
            break
        except:
            if conn_tries == num_tries - 1:
                return None
            else:
                time.sleep(1)
    return connection

def main():
    conn = connect_db(db_config)
    repl(conn)


if __name__ == '__main__':
    main()