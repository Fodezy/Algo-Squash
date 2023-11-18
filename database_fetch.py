import json
import mysql.connector

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

        ### END OF functions

        db_connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if db_connection.is_connected():
            cursor.close()
            db_connection.close()
            print("MySQL connection is closed")
