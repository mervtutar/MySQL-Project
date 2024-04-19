import mysql.connector
from ibookdb import IBOOKDB
from queryresult import QueryResult

class BOOKDB(IBOOKDB):

    def __init__(self,user,password,host,database,port):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.port = port
        self.connection = None

    def initialize(self):
        self.connection = mysql.connector.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database,
            port=self.port
        )

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()


    def createTables(self):
        pass

    def dropTables(self):
        pass

    def insertAuthor(self,authors):
        pass
      
    def insertBook(self,books):
        pass
    def insertPublisher(self,publishers):
        pass
    def insertAuthor_of(self,author_ofs):
        pass
    def functionQ1(self):
        pass
    def functionQ2(self,author_id1, author_id2):
        pass
    def functionQ3(self,author_name):
        pass
    def functionQ4(self):
        pass
    def functionQ5(self,author_id):
        pass
    def functionQ6(self):
        pass
    def functionQ7(self,rating):
        pass
    def functionQ8(self):
        pass
    def functionQ9(self,keyword):
        pass
    def function10(self):
        pass
