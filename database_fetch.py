import json
import mysql.connector

def load_server():
    """Load data from the SquashNoFriends database."""
    try:
        # Connect to the database
        db_connection = mysql.connector.connect(
            host="34.42.173.231",
            user="root",
            password="BIUouwbwi739372",
            database="SquashNoFriends"
        )
        cursor = db_connection.cursor()
        
        # Extract data using a helper function
        extracted_raw_data = extract_data_query(cursor)
        
        # Commit changes if any were made during data extraction
        db_connection.commit()

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return None

    finally:
        # Ensure the database connection is closed
        if db_connection.is_connected():
            cursor.close()
            db_connection.close()
            print("MySQL connection is closed.")

    return extracted_raw_data

def extract_data_query(cursor):
    """Extract and process user data from the SQL cursor."""
    cursor.execute("SELECT id, availability, email, name FROM submissions")
    result = cursor.fetchall()
    data = {}

    for row in result:
        user_id, availability, email, name = row
        
        # Only proceed if availability is not None
        if availability is not None:
            try:
                availability_dict = json.loads(availability)
            except json.JSONDecodeError:
                print(f"Error decoding JSON for user ID {user_id}")
                continue  # Skip this user and continue with the next
        else:
            availability_dict = {}

        # Check if the email and name are not empty strings
        if email and name:
            # Compile the user data into the dictionary
            data[user_id] = {
                'availability': availability_dict,
                'email': email,
                'name': name,
            }

    return data

# Load data from the server
data = load_server()

# Print the data for inspection (use items() for dictionary iteration)
for user_id, details in data.items():
    print(f"User ID {user_id}:")
    print(json.dumps(details, indent=4), '\n')
