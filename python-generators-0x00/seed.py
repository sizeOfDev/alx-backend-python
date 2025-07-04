#!/usr/bin/python3
import mysql.connector
import os
import csv
import uuid
from decimal import Decimal

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
        cursor.close()

def insert_data(connection, csv_file_path):
    try:
        cursor = connection.cursor()

        with open(csv_file_path, 'r') as file:
            csv_reader = csv.DictReader(file)

            for row in csv_reader:
                email = row['email'].strip()

                # Check for duplicate
                cursor.execute("SELECT user_id FROM user_data WHERE email = %s", (email,))
                if cursor.fetchone():
                    print(f"Skipping duplicate: {email}")
                    continue

                try:
                    user_id = str(uuid.uuid4())
                    name = row['name'].strip()
                    age = Decimal(row['age'])

                    cursor.execute("""
                        INSERT INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                    """, (user_id, name, email, age))

                except (ValueError, KeyError) as e:
                    print(f"Skipping row due to error: {e} - Row: {row}")
                    continue

        connection.commit()
        print("Successfully inserted user records.")

    except mysql.connector.Error as e:
        connection.rollback()
        print(f"Error during data insertion: {e}")
    finally:
        cursor.close()


