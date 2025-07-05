from seed import connect_to_prodev

def stream_user_ages():
    """
    Stream users with ages from the ProDev database.
    
    Yields:
        dict: A dictionary containing user_id, name, email, and age.
    """
    db = connect_to_prodev()
    cursor = db.cursor()
    
    cursor.execute("SELECT age FROM users")
    users = cursor.fetchall()
    
    for (age,) in users:
        yield {
            "age": int(age)
        }
    
    cursor.close()
    db.close()
def average_age():
    """
    calculate the average age of users.
    """
    ages = stream_user_ages()
    
    total_age = 0
    count = 0

    for age in ages:
        total_age += age['age']
        count += 1
    
    print(f"Average age of users is: {total_age/count:.2f}")

if __name__ == "__main__":
    average_age()    