import sqlite3 
from functools import wraps

def with_db_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with sqlite3.connect('users.db') as conn:
            kwargs['conn'] = conn
        return func(*args, **kwargs)
    return wrapper

def transactional(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = kwargs['conn']

        if conn is None:
            print('Database connection not established')
        try:
            result = func(*args, **kwargs)
            conn.commit()
            print('transction commited succesfully')
            return result
        except sqlite3.Error as e:
            conn.rollback()
            print(f'Calling ROLLBACK \nError: {e}')
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
#### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')