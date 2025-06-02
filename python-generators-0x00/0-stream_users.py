#!/usr/bin/python3
import mysql.connector
seed = __import__('seed')

def stream_users():
    """A generator that fetches rows one by one from the `user_data` table.
    """
    try:
        connection = seed.connect_to_prodev()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM user_data;")
        for row in cursor:
            yield row
    except mysql.connector.Error as err:
        print(f"{err.__class__.__name__}: {err}")
    finally:
        if connection:
            connection.close()
