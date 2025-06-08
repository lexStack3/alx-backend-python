#!/usr/bin/python3
"""Creats a decorator that manages database transactions by automatically
committing or rolling back changes.
"""
import sqlite3
import functools


def with_db_connection(func):
    """Authomatically handles opening and closing database connections.
    """
    @functools.wraps(func)
    def wrapper_with_db_connection(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        result = func(conn, *args, **kwargs)
        conn.close()
        return result
    return wrapper_with_db_connection

def transactional(func):
    """Manages database transactiosn by automatically commiting or rolling
    back changes.
    Args:
        func (callable): Function to wrap.
    Returns:
        Decorator.
    """
    @functools.wraps(func)
    def wrapper_transactional(*args, **kwargs):
        conn = kwargs.get('conn', None)
        if conn is None:
            conn = args[0]

        try:
            result = func(*args, **kwargs)
            conn.commit()
            return result
        except (sqlite3.OperationalError,
                sqlite3.IntegrityError,
                sqlite3.ProgrammingError,
                sqlite3.DatabaseError,
                sqlite3.InterfaceError) as err:
            conn.rollback()
            raise
    return wrapper_transactional

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

##### Update user's email with automatic transaction handling

update_user_email(user_id=1, new_email='Crawford_cartwright@hotmail.com')
