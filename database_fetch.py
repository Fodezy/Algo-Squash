import json
import mysql.connector

# Function to load data from the server
def LoadServer():
    try:
        # Establish a connection to the MySQL database
        db_connection = mysql.connector.connect(
            host="34.42.173.231",
            user="root",
            password="BIUouwbwi739372",
            database="SquashNoFriends"
        )
        cursor = db_connection.cursor()

        # Extract data from the database
        extracted_raw_data = extract_data_query(cursor)

        # Commit any changes to the database
        db_connection.commit()
    except mysql.connector.Error as err:
        # Print any errors that occur during the connection or data extraction
        print(f"Error: {err}")
        return -1
    finally:
        # Close the database connection
        if db_connection.is_connected():
            cursor.close()
            db_connection.close()
            print("MySQL connection is closed")
            # Return the extracted data
            return extracted_raw_data

# Function to extract data from the database
def extract_data_query(cursor):
    # Execute the SQL query to select data
    cursor.execute("SELECT id, availability, email, name FROM submissions")

    # Fetch all the rows returned by the database
    result = cursor.fetchall()
    data = {}  # Initialize as an empty dictionary to store the data

    # Process each row in the result
    for row in result:
        id, availability, email = row
        # Convert the JSON string in 'availability' to a dictionary
        availability_dict = json.loads(availability)
        # Store each user's data with their 'id' as the key
        data[id] = {
            'availability': availability_dict,
            'email': email,
            'name': name,
        }
    # Return the processed data
    return data   

# Uncomment the line below to execute the LoadServer function and load data
# data = LoadServer()
