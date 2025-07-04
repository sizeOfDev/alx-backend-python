from seed import connect_to_prodev

def stream_users():
    """
    Generator function to stream users from the database
    """
    connection = connect_to_prodev()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data")
        for row in cursor:
            yield row
        cursor.close()
        connection.close()
    else:
        print("Failed to connect to the database.")


if __name__ == '__main__':
    from itertools import islice
    for user in islice(stream_users(), 6):
        print(user)
        


