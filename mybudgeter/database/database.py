import os
import datetime
import sqlite3

class Database(object):
    def __init__(self, file_path, db=None) -> None:
        if db:
            self.connect(db)
        else:
            self.create_db(file_path)
    
    def connect(self, db):
        self.cnx = sqlite3.connect(db)
        self.cur = self.cnx.cursor()

    def close(self):
        self.cnx.close()

    def __del__(self):
        self.close()

    def query(self, query, args=None):
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