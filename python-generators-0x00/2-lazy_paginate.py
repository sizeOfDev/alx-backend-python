from seed import connect_to_prodev

def paginate_users(page_size, offset):
    """
    Paginate users from the ProDev database.
    
    Args:
        page_size (int): The number of users to fetch in each page.
        offset (int): The offset for pagination.
    
    Yields:
        list: A list of user dictionaries.
    """
    db = connect_to_prodev()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM users LIMIT %s OFFSET %s", (page_size, offset))
    users = cursor.fetchall()
    
    if not users:
        return
    
    for user in users:
        yield {
            "user_id": user[0],
            "name": user[1],
            "email": user[2],
            "age": int(user[3])
        }
    
    cursor.close()
    db.close()

def lazy_paginate(page_size):
    """
    Lazy paginate users.
    
    Args:
        page_size (int): The number of users to fetch in each page.
    
    Yields:
        list: A list of user dictionaries.
    """
    offset = 0
    while True:
        users = list(paginate_users(page_size, offset))
        if not users:
            break
        yield users
        offset += page_size


if __name__ == "__main__":
    page_size = 100
    for users in lazy_paginate(page_size):
        for user in users:
            if user['age'] >= 25:
                print(user)