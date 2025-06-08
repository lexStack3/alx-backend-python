#!/usr/bin/python3
"""Creates a decorator that retries database operations if they fail due to
    transient errors.
"""
import time
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

def retry_on_failure(retries, delay):
    """Implements the <retry_on_failure> decorator."""
    def retry_on_failure_decorator(func):
        """Creates a decorator that retries database operations if they
        fail due to transient errors.
        """
        @functools.wraps(func)
        def wrapper_retry_on_failure(*args, **kwargs):
            last_exception = None
            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except (sqlite3.OperationalError,
                        sqlite3.IntegrityError,
                        sqlite3.ProgrammingError,
                        sqlite3.DatabaseError,
                        sqlite3.InterfaceError) as err:
                    last_exception = err
                    time.sleep(delay)
            raise last_exception
        return wrapper_retry_on_failure
    return retry_on_failure_decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)
