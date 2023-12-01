import os
import datetime
import sqlite3

def sql_query(cursor, query, args=None):
    try:
        if args:
            cursor.execute(query, args)
        else:
            cursor.execute(query)
    except sqlite3.Error as err: 
            print(err)
        
class Transactions(object):
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
        db = os.path.join(file_path, "transactions.db")
        try:
            self.__connect(db)
            self.__cur.execute("""CREATE TABLE transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    trans_date date,
                    name text,
                    category text,
                    amount decimal(7,2))""")
            self.__cnx.commit()
        except sqlite3.Error as err: 
            print(err) 
            self.__close()

    def add_transaction(self, category, amount, date=None, name=None):
        if isinstance(date, datetime.datetime):
            # convert to string for sql
            date = date.strftime("%Y-%m-%d")
        elif date is None:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
    
        tup = (category.lower(), amount, date, name)

        # sql statement
        try:
            self.__cur.execute("""INSERT INTO transactions (category, amount, trans_date, name) 
                                     VALUES (?, ?, ?, ?) RETURNING id""", tup)
            res = self.__cur.fetchone()[0]
            self.__cnx.commit()
            return res
        except sqlite3.Error as err: 
            print(err)

    def modify_transaction(self, id, field, value):
        # change some part of the transaction
        query = f"update transactions set {field} = ? WHERE id = ?"
        args = (value, id)
        sql_query(self.__cur, query, args)
        self.__cnx.commit()

    def delete_transaction(self, id):
        query = """delete from transactions WHERE id = ?"""
        args = (id,)
        sql_query(self.__cur, query, args)
        self.__cnx.commit()

    def get_categories(self):

        query = """SELECT DISTINCT category from transactions"""
        sql_query(self.__cur, query)
        return [cat[0] for cat in self.__cur]
    
    def get_n_transactions(self, n, sort_field='trans_date', asc=False):
        if asc:
             query = f'SELECT * from transactions order by {sort_field} limit {n}'
        else:
            query = f'SELECT * from transactions order by {sort_field} DESC limit {n}'
        sql_query(self.__cur, query)
        return [cat for cat in self.__cur]