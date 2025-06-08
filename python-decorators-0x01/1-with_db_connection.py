#!/usr/bin/python3
"""Creates a decorator that authomatically handles opening and closing database connections.
"""
import sqlite3
import functools


def with_db_connection(func):
    """Authomatically handles opening and closing database connections.
    """
    @functools.wraps(func)
    def wrapper_with_db_connection(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper_with_db_connection

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchall()
#### Fetch user by ID with automatic connection handling

user = get_user_by_id(user_id=1)
print(user)
