import mysql.connector
import time

conn_tries = 0
for conn_tries in range(0, 10):
    try:
        config = {
            'user': 'root',
            'password': 'root',
            'host': 'db',
            'port': '3306',
            'database': 'knights'
        }
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM favorite_colors')
        results = [{name: color} for (name, color) in cursor]
        cursor.close()
        connection.close()

        print(results)
        break
    except:
        time.sleep(1)

if conn_tries == 9:
    print("Failed to connect to database")
    exit(1)


