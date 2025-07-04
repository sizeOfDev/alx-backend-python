#!/usr/bin/python3
import mysql.connector
import os

def connect_db():
    """
    connect to database server
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASS", "secret")
        )
        if connection.is_connected():
            print("Connected to Database server")
            return connection
    except mysql.connector.Error as e:
        print(f"database error {e}")
        return None
    
def create_database(connection):
    """
    Create datbase if not exists
    """
    connection = connect_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database created | Database Already exists")
        connection.close

def connect_to_prodev():
    """
    connect to ALX_prodev database
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASS", "secret"),
            database="ALX_prodev"
        )
        if connection.is_connected():
            print("Connected to ALX_prodev database")
            return connection
    except mysql.connector.Error as e:
        print(f"database error {e}")
        return None

def create_table(connection):
    """
    Create table if not exists
    """
    connection = connect_to_prodev()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
           CREATE TABLE IF NOT EXISTS user_data (
           user_id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
           name VARCHAR(255) NOT NULL,
           email VARCHAR(255) NOT NULL,
           age DECIMAL NOT NULL,
           INDEX (user_id)
            )
        """)
        print("Table created | Table Already exists")
        connection.close()

def insert_data(connection, data):
    """
    Insert data into table
    """
    connection = connect_to_prodev()
    if connection:
        cursor = connection.cursor()
        query = "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)"
        cursor.execute(query, data)
        connection.commit()
        print("Data inserted successfully")
        connection.close()