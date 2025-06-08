#!/usr/bin/python3
"""Creates a decorator that caches the results of a database queries inorder to avoid redundant calls.
"""
import time
import sqlite3
import functools


query_cache = {}

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

def cache_query(func):
    @functools.wraps(func)
    def wrapper_cache_query(*args, **kwargs):
        key = kwargs.get('query') if 'query' in kwargs else args[0]
        if key in query_cache.keys():
            return query_cache[key]
        time.sleep(2)
        result = func(*args, **kwargs)
        query_cache[key] = result
        return result
    return wrapper_cache_query

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call with cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)
#### Second call with the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)
third_user = fetch_users_with_cache(query="SELECT * FROM users")
print(third_user)
