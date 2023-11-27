class Budget(object):
    def __init__(self, n_categories=1) -> None:
        self.n_categories = n_categories
        self.budget = self.new_budget(self.n_categories)
        self.spending = self.get_spending()
    
    def new_budget(n):
        # get user to give n category names and limits
        pass

    def get_spending():
        # need a way to calculate user spending
        pass

    def check_budget():
        # print info about budget
        pass

    def modify():
        # change some part of the budget
        pass

    def save():
        # save budget info
        pass

    def load():
        # load in a budget
        pass
