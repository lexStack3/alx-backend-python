#!/usr/bin/python3
"""Creates a reusable context manager that takes a query as input and
execute it, managing both connection and the query execution.
"""
import sqlite3


class ExecuteQuery():
    """A reusable context manager that takes a query as input
    and executes it, managing both connection and the query execution
    """
    def __init__(self, query, /, *args):
        """Creates an instance of the class with passed arguments.
        Args:
            query (str): Query to execute
            args (int, decimal, str): Parameters for <query>
        """
        self.__conn = sqlite3.connect('users.db')
        self.__query = query
        self.__parameters = tuple(args) or ()

    def __enter__(self):
        cursor = self.__conn.cursor()
        cursor.execute(self.__query, self.__parameters)
        return cursor.fetchall()

    def __exit__(self, type, value, traceback):
        self.__conn.close()


if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    age = 25
    with ExecuteQuery(query, age) as result:
        for item in result:
            print(item)
