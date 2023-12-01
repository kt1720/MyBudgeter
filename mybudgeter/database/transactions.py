import os
import datetime
import sqlite3

from database.database import Database
        
class Transactions(Database):
    def __init__(self, file_path, db=None) -> None:
        super().__init__(file_path, db)

    def __create_db(self, file_path):
        db = os.path.join(file_path, "transactions.db")
        query = """CREATE TABLE transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    trans_date date,
                    name text,
                    category text,
                    amount decimal(7,2))"""
        try:
            self.query(query)
            self.cnx.commit()
        except sqlite3.Error as err: 
            print(err) 
            self.close()

    def add_transaction(self, category, amount, date=None, name=None):
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

    def modify_transaction(self, id, field, value):
        # change some part of the transaction
        query = f"update transactions set {field} = ? WHERE id = ?"
        args = (value, id)
        self.query(query, args)
        self.cnx.commit()

    def delete_transaction(self, id):
        query = """delete from transactions WHERE id = ?"""
        args = (id,)
        self.query(query, args)
        self.cnx.commit()

    def get_categories(self):

        query = """SELECT DISTINCT category from transactions"""
        self.query(query)
        return [cat[0] for cat in self.cur]
    
    def get_n_transactions(self, n, sort_field='trans_date', asc=False):
        if asc:
             query = f'SELECT * from transactions order by {sort_field} limit {n}'
        else:
            query = f'SELECT * from transactions order by {sort_field} DESC limit {n}'
        self.query(query)
        return [cat for cat in self.cur]