import sqlite3 
from functools import wraps

def with_db_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with sqlite3.connect('users.db') as conn:
            kwargs['conn'] = conn
        return func(*args, **kwargs)
    return wrapper
        
@with_db_connection 
def get_user_by_id(conn, user_id): 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchone()
 
#### Fetch user by ID with automatic connection handling 

user = get_user_by_id(user_id=1)
print(user)