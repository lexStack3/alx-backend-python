#!/usr/bin/python3
"""Creates a class based context manager to handle opening and closing database 
connections automatically.
"""
import functools
import sqlite3


class DatabaseConnection():
    """A database context manager for opening and closing
    database connections automatically.
    """
    def __init__(self):
        self.__conn = sqlite3.connect('users.db')

    def __enter__(self):
        return self.__conn

    def __exit__(self, type, value, traceback):
        self.__conn.close()


if __name__ == "__main__":
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()

for user in users:
    print(user)
