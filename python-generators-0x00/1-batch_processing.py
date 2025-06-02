#!/usr/bin/python3
"""Creates a generator to fetch and process data in batches from the users database.
"""
import mysql.connector
seed = __import__('seed')

def stream_users_in_batches(batch_size):
    """Fetches rows in batches:
    Args:
        batch_size (int): Batch size.
    """
    try:
        connection = seed.connect_to_prodev()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM user_data;")

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
    except mysql.connector.Error as err:
        print(f"{err.__class__.__name__}: {err}")
    finally:
        if connection:
            connection.close()


def batch_processing(batch_size):
    """Processes each batch to filter users over the age of 25.
    Args:
        batch_size (int): Batch Size.
    """
    for batch in stream_users_in_batches(batch_size):
        filtered = [user for user in batch if user.get('age') > 25]
        for user in filtered:
            print(user)
