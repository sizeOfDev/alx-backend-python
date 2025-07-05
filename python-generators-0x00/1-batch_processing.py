from seed import connect_to_prodev

def stream_users_in_batches(batch_size):
    """
    Stream users in batches from the ProDev database.
    
    Args:
        batch_size (int): The number of users to fetch in each batch.
    
    Yields:
        list: A list of user dictionaries.
    """
    db = connect_to_prodev()
    cursor = db.cursor()
    
    offset = 0
    while True:
        cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (batch_size, offset))
        users = cursor.fetchall()
        
        if not users:
            break
        
        yield users
        offset += batch_size
    
    cursor.close()
    db.close()

def batch_processing(batch_size):
    """
    Process users in batches.
    
    Args:
        batch_size (int): The number of users to process in each batch.
    """
    for users in stream_users_in_batches(batch_size):
        for user in users:
           if user[3] >= 25:
               yield {
                   "user_id": user[0],
                   "name": user[1],
                   "email": user[2],
                   "age": int(user[3])
               }

if __name__ == "__main__":
    batch_size = 100
    for user in batch_processing(batch_size):
        print(user)