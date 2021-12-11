import mysql.connector
from database.Connector import DBConnector

class UpdateTable(DBConnector):
    def notification(self, notif, newLimitPrice):
        query = "UPDATE notifications SET price_limit = %s WHERE id = %s"
        value = [newLimitPrice, notif['id']]
        try :
            self.connection.execute(query, tuple(value))
            self.mydb.commit()
        except mysql.connector.Error as err:
            print(err.msg)

        self.closeConnection()