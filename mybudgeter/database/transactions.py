import os
import datetime
import sqlite3

from database.database import Database
        
class Transactions(Database):
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
        db = os.path.join(file_path, "transactions.db")
        query = """CREATE TABLE transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    trans_date date,
                    name text,
                    category text,
                    amount decimal(7,2))"""
        try:
            self.connect(db)
            self.query(query)
            self.cnx.commit()
        except sqlite3.Error as err: 
            print(err) 
            self.close()

    def add_transaction(self, category:str, amount:float, date=None, name=None):
        """Adds an individual transaction to the transactions table and returns the transaction id when successful.
        Date can be a datetime object or None which defaults to the current date. 
        Name is an optional string parameter to store info about the transaction more info."""
        
        if isinstance(date, datetime.datetime):
            # convert to string for sql
            date = date.strftime("%Y-%m-%d")
        elif date is None:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
    
        args = (category.lower(), amount, date, name)

        # sql statement
        query = """INSERT INTO transactions (category, amount, trans_date, name) 
                                     VALUES (?, ?, ?, ?) RETURNING id"""
        self.query(query, args)
        res = self.cur.fetchone()[0]
        self.cnx.commit()
        return res

    def modify_transaction(self, id:int, field:str, value):
        """Modifies the value of the given field for the transaction in the table with id."""
        # change some part of the transaction
        query = f"update transactions set {field} = ? WHERE id = ?"
        args = (value, id)
        self.query(query, args)
        self.cnx.commit()

    def delete_transaction(self, id:int):
        "Deletes a transaction from the table."
        query = """delete from transactions WHERE id = ?"""
        args = (id,)
        self.query(query, args)
        self.cnx.commit()

    def get_categories(self):
        "Returns a list of unique categories that are in the transaction table."

        query = """SELECT DISTINCT category from transactions"""
        self.query(query)
        return [cat[0] for cat in self.cur]
    
    def get_n_transactions(self, n:int, sort_field='trans_date', asc=False):
        "Returns a list of n transactions sorted by the sort_field."
        if asc:
             query = f'SELECT * from transactions order by {sort_field} limit {n}'
        else:
            query = f'SELECT * from transactions order by {sort_field} DESC limit {n}'
        self.query(query)
        return [cat for cat in self.cur]