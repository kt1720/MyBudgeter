import os
import datetime
import sqlite3

class Database(object):
    "A base class for database objects to inherit from."
    def __init__(self, file_path=None, db=None) -> None:
        """Initialize the database either by providing a file_path where a 
        new database will be created or provide the path to an existing db."""
        # set as current working directory if none provided
        file_path = file_path if file_path else os.getcwd()
        if db:
            self.connect(db)
        else:
            self.__create_db(file_path)
    
    def connect(self, db):
        "Create a connection to the db."
        self.cnx = sqlite3.connect(db)
        self.cur = self.cnx.cursor()

    def close(self):
        "Close the db connections."
        self.cnx.close()

    def __del__(self):
        self.close()

    def query(self, query, args=None):
        """Query the db with optional arguments. Query is executable and SQL
          statement and args should be a tuple."""
        try:
            if args:
                self.cur.execute(query, args)
            else:
                self.cur.execute(query)
        except sqlite3.Error as err: 
            print(err)

    def __create_db(self, file_path):
        pass

    def get_categories(self):
        pass