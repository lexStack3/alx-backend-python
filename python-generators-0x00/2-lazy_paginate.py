#!/usr/bin/python3
"""Simulate fetching paginated data from the users database using a 
generator to lazily load each page.
"""
seed = __import__('seed')


def paginate_users(page_size, offset):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows

def lazy_pagination(page_size):
    """Simulates fetching paginated data from the ALX_prodev
    database.

    Args:
        page_size (int): Size data to fetch.
    """
    offset = 0
    rows = paginate_users(page_size, offset)
    while rows:
        offset += len(rows)
        yield rows
        rows = paginate_users(page_size, offset)
