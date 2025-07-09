import time
import sqlite3 
from functools import wraps


query_cache = {}

def with_db_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with sqlite3.connect('users.db') as conn:
            kwargs['conn'] = conn
        return func(*args, **kwargs)
    return wrapper

def cache_query(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        query = kwargs.get('query')
        
        if query in query_cache:
            return (query_cache[query])
        
    
        result = func(*args, **kwargs)
        query_cache[query] = result

        print(f'Cached queries: {query_cache}')
        return result
    return wrapper

def timer(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            return result
        finally: 
            end_time = time.perf_counter()
            duration = end_time - start_time
            print(f"Function '{func.__name__}' executed in {duration:.4f} seconds.")
    return wrapper

@timer
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")