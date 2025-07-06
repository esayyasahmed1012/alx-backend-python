# 2-lazy_paginate.py

import seed

def paginate_users(page_size, offset):
    """
    Fetch a page of users from the database.
    
    Args:
        page_size (int): Number of users to fetch per page.
        offset (int): Starting index for the page.
    
    Returns:
        list: A list of user dictionaries.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows

def lazy_paginate(page_size):
    """
    Generator function to lazily paginate users from the database, starting at offset 0.
    
    Args:
        page_size (int): Number of users to fetch per page.
    
    Yields:
        list: A page of user dictionaries.
    """
    offset = 0
    while True:  # Single loop to fetch pages
        page = paginate_users(page_size, offset)
        if not page:  # Stop if no more data
            break
        yield page
        offset += page_size

if __name__ == "__main__":
    # Example usage for testing
    for page in lazy_paginate(100):
        for user in page:
            print(user)