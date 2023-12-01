import os
import datetime
import sqlite3

class Database(object):
    def __init__(self, file_path, db=None) -> None:
        if db:
            self.__connect(db)
        else:
            self.__create_db(file_path)
    
    def __connect(self, db):
        self.__cnx = sqlite3.connect(db)
        self.__cur = self.__cnx.cursor()

    def __close(self):
        self.__cnx.close()

    def __del__(self):
        self.__close()

    def __query(self, query, args=None):
        try:
            if args:
                self.__cur.execute(query, args)
            else:
                self.__cur.execute(query)
        except sqlite3.Error as err: 
            print(err)

    def __create_db(self, file_path):
        pass

    def get_categories(self):
        pass