import mysql.connector
from database.Connector import DBConnector

class InsertTable(DBConnector):
    def headline(self, headlines):
        query = "INSERT IGNORE INTO headlines (\
            channel_name ,original_link, title, image, author, editor, content, publish_date, created_at)\
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = []
        for headline in headlines:
            values.append(headline.toTuple())

        try :
            self.connection.executemany(query, values)
            self.mydb.commit()
        except mysql.connector.Error as err:
            print(err.msg)

        self.closeConnection()

    def analytics(self, analytic):
        query = "INSERT INTO analytic_common_words (content, created_at) VALUES (%s, %s)"
        value = analytic.toTuple()
        try :
            self.connection.execute(query, value)
            self.mydb.commit()
        except mysql.connector.Error as err:
            print(err.msg)

        self.closeConnection()