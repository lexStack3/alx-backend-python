#!/usr/bin/python3
import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector.connection_cext import CMySQLConnection
from uuid import uuid4
import csv
import os

config = {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWD'),
        'port': os.getenv('DB_PORT')
        }

def connect_db():
    """Connects to a MySQL Database Server."""
    if not all(config.values()):
        raise EnvironmentError("Some required environmental variables missing.")
    connection = mysql.connector.connect(**config)
    return connection

def create_database(connection):
    """Creates the database `ALX_prodev` it it does not exist.
    
    Args:
        connection (MySQLConnection): MySQL Database - ALX_prodev

    Returns:
        connection
    """
    if isinstance(connection, (MySQLConnection, CMySQLConnection)):
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS `ALX_prodev`;")
        connection.commit()
        return connection
    else:
        return False


def connect_to_prodev():
    """Connects to the ALX_prodev database in MySQL."""
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("USE ALX_prodev;")
    return connection

def create_table(connection):
    """Creates a table [user_data] if it does not exists.
        - user_id(Primary Key, UUID, Indexed
        - name (VARCHAR, NOT NULL)
        - email (VARCHAR, NOT NULL)
        - age (INT, NOT NULL)
    """
    if isinstance(connection, (MySQLConnection, CMySQLConnection)):
        queryStr = """
        CREATE TABLE IF NOT EXISTS `user_data` (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(256) NOT NULL,
        email VARCHAR(256) NOT NULL,
        age INT NOT NULL
        ) ENGINE=InnoDB;
        """
        cursor = connection.cursor()
        cursor.execute(queryStr)
        connection.commit()
        print("Table user_data created successfully")

def insert_data(connection, data):
    """Inserts data into the `user_data` table.

    Args:
        connection (MySQLConnection): A MySQL Database - ALX_prodev
        data (str): Name of the csv file to copy data from.

    Returns:
        None
    """
    if isinstance(connection, (MySQLConnection, CMySQLConnection)):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data;")
        old_users = cursor.fetchall()

        with open(data, mode='r', newline='', encoding='utf-8') as file:
            users = csv.DictReader(file)
            for user in users:
                name = user.get('name')
                email = user.get('email')
                age = int(user.get('age'))

                old_user = [person for person in old_users if person[1] == name and
                            person[2] == email and int(person[3]) == age]
                if old_user:
                    continue
                queryStr = """
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s);
                """
                cursor.execute(queryStr, (str(uuid4()), name, email, age))
        connection.commit()
