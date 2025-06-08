#!/usr/bin/python3
"""Creates a decorator that logs database queries executed by any function.
"""
import sqlite3
import functools
from datetime import datetime
import sys, os


def log_queries(func):
    """Logs database queries executed by any function.
    Args:
        func (callable): Function to decorate.

    Return:
        Decorated version of <func>.
    """
    @functools.wraps(func)
    def wrapper_log_queries(*args, **kwargs):
        query = kwargs.get('query', None)
        if query is None and len(args) > 0:
            query = args[0]
        timestamp = datetime.now().strftime("%b %d %H:%M:%S")
        try:
            username = os.getlogin()
        except OSError:
            import getpass
            username = getpass.getuser()
        filename = os.path.basename(sys.argv[0])
        pid = os.getpid()
        log = "{} {} {}[{}]: SQL query executed: {}".format(timestamp,
                   username,
                   filename,
                   pid,
                   query)
        print(log)
        func(*args, **kwargs)
    return wrapper_log_queries


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
