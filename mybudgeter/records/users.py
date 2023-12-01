import os

from budget import Budget
from transactions import Transactions

class User(object):
    def __init__(self, file_path=None, db=None, budget=None, transactions=None) -> None:
        self.file_path = os.getcwd() if not file_path else file_path
        if db: # we assume the db has both tables
            self.budget = Budget(self.file_path, db=db)
            self.transactions = Transactions(self.file_path, db=db)
        else:
            # when budget is none, create new db, else can be a Budget object, or a path to budget db
            if isinstance(budget, Budget):
                self.budget = budget
            elif isinstance(budget, str):
                self.budget = Budget(self.file_path, budget)
            else:
                self.budget = Budget(self.file_path)
            
            if isinstance(transactions, Transactions):
                self.transactions = transactions
            elif isinstance(transactions, str):
                self.transactions = Transactions(self.file_path, transactions)
            else:
                self.transactions = Transactions(self.file_path)

