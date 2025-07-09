import time
import sqlite3 
from functools import wraps

def with_db_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with sqlite3.connect('users.db') as conn:
            kwargs['conn'] = conn
        return func(*args, **kwargs)
    return wrapper

def retry_on_failure(retries, delay):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            attempt = 0
            while attempt < retries:
                try:
                    return result
                except sqlite3.Error as e:
                    attempt += 1
                    print(f"Attempt {attempt} failed: {e}. Retrying in {delay} seconds...")
                    time.sleep(delay)

            print(f"All {retries} attempts failed. Exiting.")
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM userss")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)