import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
from pathlib import Path
import os

class DBConnector:
    
    def __init__(self):
        env_path = str(Path('.') / '.env')
        load_dotenv(dotenv_path=env_path)
        
        try :
            self.mydb = mysql.connector.connect(
                host = os.getenv("DB_HOST"),
                database = os.getenv("DB_DATABASE"),
                user= os.getenv("DB_USERNAME"),
                password = os.getenv("DB_PASSWORD")
            )
            self.connection = self.mydb.cursor(dictionary=True)

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print("Connection problem : " + err)

    def closeConnection(self):
        self.connection.close()
        self.mydb.close()