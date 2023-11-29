import os
import datetime
import sqlite3

class Budget(object):
    def __init__(self, file_path, db=None) -> None:
        if db:
            self.__connect(db)
        else:
            self.create_db(file_path)
        

    def __connect(self, db):
        self.__cnx = sqlite3.connect(db)
        self.__cur = self.__cnx.cursor()

    def __close(self):
        self.__cnx.close()

    def __del__(self):
        self.__close()

    def create_db(self, file_path):
        db = os.path.join(file_path, "budgeting.db")
        try:
            self.__connect(db)
            self.__cur.execute("""CREATE TABLE budget (
                            category text,
                            month int,
                            year int,
                            amount decimal(7,2),
                            PRIMARY KEY (category,month,year),
                            CHECK (month >= 1 AND month <= 12 AND year > 0)
                            );""")
            self.__cnx.commit()
        except sqlite3.Error as err: 
            print(err)
            self.__close()

    def add_category(self, category, limit=0, date=None):
        date = datetime.datetime.now() if date is None else date
        tup = (category.lower(), date.month, date.year, limit)
        try:
            self.__cur.execute(
                """INSERT INTO budget 
                (category, month, year, amount) 
                VALUES (?, ?, ?, ?)""", tup)
            self.__cnx.commit()
        except sqlite3.Error as err: 
            print(err)

    def add_from_lists(self, cat_list, limit_list=None, date_list=None):
        
        # check lists are same length and if not given, create default list
        if isinstance(limit_list, list):
            if not len(cat_list) == len(limit_list):
                raise Exception("The lists need to be the same length.")
        else:
            limit_list = [0]*len(cat_list)
            
        if isinstance(date_list, list):
            if not len(cat_list) == len(date_list):
                raise Exception("The lists need to be the same length.")
        else:
            date_list = [datetime.datetime.now()]*len(cat_list)
        
        # add to table
        for i in range(len(cat_list)):
            self.add_category(cat_list[i], limit_list[i], date_list[i])
    
    def modify_category():
        # change some part of the budget
        pass

    def delete_category():
        pass


    def check_budget():
        # print info about budget
        pass