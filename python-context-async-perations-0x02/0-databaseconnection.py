class DatabaseConnection():

    def __init__(self, databaseName):
        self.databaseName = databaseName

    def __enter__(self):
        import sqlite3
        self.database = sqlite3.connect(self.databaseName)
        return self.database

    def __exit__(self, exc_type, exc_val, traceback ):
        self.database.close()


def fetch_all_users(query):
    with DatabaseConnection('users.db') as conn:
        cursor = conn.cursor()   
        cursor.execute(query)
        results = cursor.fetchall()
        return results

users = fetch_all_users('SELECT * FROM users')

for user in users:
    print(user)