import os
import datetime
import sqlite3

from mybudgeter.database.database import Database

class Budget(Database):
    def __init__(self, file_path=None, db=None) -> None:
        """Initialize the database either by providing a file_path where a 
        new database will be created or provide the path to an existing db."""
        # set as current working directory if none provided
        file_path = file_path if file_path else os.getcwd()
        if db:
            self.connect(db)
        else:
            self.__create_db(file_path)

    def __create_db(self, file_path):
        "Create a new database and budget table to store budget information at the given file_path."
        db = os.path.join(file_path, "budgeting.db")
        query = """CREATE TABLE budget (
                            category text,
                            month int,
                            year int,
                            amount decimal(7,2),
                            PRIMARY KEY (category,month,year),
                            CHECK (month >= 1 AND month <= 12 AND year > 0)
                            );"""
        try:
            self.connect(db)
            self.query(query)
            self.cnx.commit()
        except sqlite3.Error as err: 
            print(err)
            self.close()

    def add_category(self, category:str, limit=0, date=None):
        """Add a new budget category to the budget table. 
        If no limit is given it will default to zero. 
        If no date is given the budget will be set for the current month and year.
        The date should be given as a datetime object."""

        date = datetime.datetime.now() if date is None else date
        args = (category.lower(), date.month, date.year, limit)
        query = """INSERT INTO budget 
                (category, month, year, amount) 
                VALUES (?, ?, ?, ?)"""
        self.query(query, args)
        self.cnx.commit()

    def add_from_lists(self, cat_list:list, limit_list=None, date_list=None):
        """Adds categories to the budget table from lists."""
        
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
    
    def modify_category(self, category:str, value:float, month:int, year:int):
        "Modifies the category limit for an entry in the budget table."

        query = f"update budget set amount = ? WHERE category = ? AND month = ? and year = ?"
        args = (value, category, month, year)
        self.query(query, args)
        self.cnx.commit()

    def delete_category(self, category:str, month:int, year:int):
        "Deletes a budget entry for the given category, month, year."

        query = f"delete from budget WHERE category = ? AND month = ? AND year = ?"
        args = (category, month, year)
        self.query(query, args)
        self.cnx.commit()

    def check_budget(self, month=None, year=None):
        """Returns a list of budget categories for the given month and year."""

        month = month if month else datetime.datetime.now().month
        year = year if year else datetime.datetime.now().year

        query = f"Select * from budget WHERE month = ? AND year = ?"
        args = (month, year)
        self.query(query, args)
        return [tup for tup in self.cur]
    
    def get_categories(self):
        "Returns a list of unique categories that are in the budget table."

        query = """SELECT DISTINCT category from budget"""
        self.query(query)
        return [cat[0] for cat in self.cur]