#!/usr/bin/python3
"""Objective: To use a generator to compute a memory-efficient
    aggregate function i.e average age for a large dataset.
"""
seed = __import__('seed')


def stream_user_age():
    """Yields user ages one by one."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT age FROM user_data;")
        age = cursor.fetchone()
        while age:
            yield age
            age = cursor.fetchone()
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    total_age = 0
    count = 0
    for row in stream_user_age():
        total_age += row.get('age')
        count += 1
    print("Average age of users: {}".format(total_age / count))
