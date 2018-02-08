import MySQLdb

class DB:
    def __init__(self, host, user, password, db):
        self.connection = MySQLdb.connect(host=host, user=user, passwd=password, db=db, charset='utf8mb4')
        self.cursor = self.connection.cursor()
    
    def query(self, command, args=()):
        self.cursor.execute(command, args)
        return self.cursor.fetchall()

    def close(self):
        self.connection.commit()
        self.connection.close()
