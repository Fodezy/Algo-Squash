import json
import mysql.connector

"id, email, availability, created, name, skill"

##right now im just doing id=0 user to all users [1,n]
def entity_user():

def LoadServer():
    try:
        db_connection = mysql.connector.connect(
        host="",
        user="",
        password="",
        database=""
        )
        cursor = db_connection.cursor()
        ### PLUG IN FUNCTIONS
        extract_data_queury(cursor)
        ### END OF functions

        db_connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if db_connection.is_connected():
            cursor.close()
            db_connection.close()
            print("MySQL connection is closed")

def extract_data_query(cursor):
    cursor.execute("SELECT id, availability, skill FROM submissions")
    result = cursor.fetchall()
    for x in result:
        print(x)
    return result