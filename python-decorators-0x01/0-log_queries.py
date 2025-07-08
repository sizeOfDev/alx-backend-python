import sqlite3
from functools import wraps


def log_queries(original_func):
    import logging
    logger = logging.getLogger(original_func.__name__)
    logger.setLevel(logging.INFO)
    if not logger.hasHandlers():
        handler = logging.FileHandler(f'{original_func.__name__}.log')
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    @wraps(original_func)
    def wrapper(*args, **kwargs):

        if args:
           query_to_log = args[0]
        elif 'query' in kwargs:
            query_to_log = kwargs['query']

        if query_to_log:
            logger.info(f'Executed query: {query_to_log}')
        else:
            logger.info(f'Executing function with args: {args}, kwargs: {kwargs}')
        return original_func(*args, **kwargs)
    return wrapper 

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
