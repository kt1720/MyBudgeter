class User(object):
    def __init__(self, name) -> None:
        self.name = name
        self.budget = None
        self.transactions = set()
        self.spending = None
    
    def add_transaction(trans):
        # check that it is a valid transaction
        # check if it puts user over budget
        pass

    def del_transaction(id):
        # delete transaction from set
        pass

    def edit_transaction(id):
        # change category, amount, date
        pass

    def load_transactions(csv_path):
        # load in transactions from csv
        pass

    def save_transactions(path):
        # save transactions to csv
        pass

    def set_budget():
        pass

    def check_budget():
        pass
