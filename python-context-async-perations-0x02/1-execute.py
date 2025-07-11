import sqlite3

class  ExecuteQuery():

    def __init__(self, query, param: tuple = (), db_path='users.db' ):
        self.db_path = db_path
        self.query = query
        self.param = param
        self.conn = None
        self.cursor = None 

        if not isinstance(param, (tuple, list)): 
            self.param = (param,)
    
    def __enter__(self):
        
        self.conn= sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        try:
            self.cursor.execute(self.query, self.param)    
        except sqlite3.Error as e:
            self.conn.close()
            raise e
        return self.cursor

    def __exit__(self, exc_type, exc_val, traceback):
        if self.conn:
            self.conn.close()


with ExecuteQuery('SELECT name FROM users WHERE age > ?', 25) as cursor:
    users = cursor.fetchall()
    for user in users:
        print(user)