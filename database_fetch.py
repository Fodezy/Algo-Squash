import json
import mysql.connector

#"id, email, availability, created, name, skill"

def LoadServer():
    try:
        db_connection = mysql.connector.connect(
        host="34.42.173.231",
        user="root",
        password="BIUouwbwi739372",
        database="SquashNoFriends"
        )
        cursor = db_connection.cursor()
        ### PLUG IN FUNCTIONS
        extracted_raw_data = extract_data_query(cursor)
        ### END OF functions

        db_connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return -1
    finally:
        if db_connection.is_connected():
            cursor.close()
            db_connection.close()
            print("MySQL connection is closed")
            return extracted_raw_data

def extract_data_query(cursor):
    cursor.execute("SELECT id, availability, skill FROM submissions")

    result = cursor.fetchall()
    data = {}  # Initialize as an empty dictionary
    for row in result:
        id, availability, skill = row
        availability_dict = json.loads(availability)
        data[id] = {  # Use id as the key
            'availability': availability_dict,
            'skill': skill
        }
    return data   


data = LoadServer()
print(data[16].get('availability'))
