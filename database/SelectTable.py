import mysql.connector
from database.Connector import DBConnector

class SelectTable(DBConnector):
    def allNotifications(self):
        self.query = "SELECT * FROM notifications"
        return self.execAll()

    def execAll(self):
        try :
            self.connection.execute(self.query)
            result = self.connection.fetchall()

            return result
        except mysql.connector.Error as err:
            print(err.msg)

        self.closeConnection()