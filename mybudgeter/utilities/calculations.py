from records.budget import Budget
from records.transactions import Transactions
class calculator():
    def __init__(self, spending, budget, categories) -> None:
        self.spending = spending,
        self.budget = budget
        self.categories = categories
    
    def total_spending(self) -> float: 
        """Calculate the total spending of the user under all categories"""
        for category in self.category:
            total_spending += self.spending[category]
            return total_spending
    
    def total_budget(self) -> float:
        """Calculate the total budget of the user under all categories"""
        for category in self.category:
            total_budget += self.budget[category]
            return total_budget
    
    def difference(self, categorize = False) -> float:
        """
        Calculate if the user is over or under budget in the given month and calculate the difference,
        user can choose whether to calculate the total or categorical difference
        warn the user if the user is overbudget
        """
        if categorize:
            categorize_diff = dict()
            for category in self.category:
                categorize_diff[category] = self.budget[category] - self.spending[category]
                if categorize_diff[category] < 0:
                    print(f"{category} is overbudget by ${categorize_diff[category]} for the current month.")
                return categorize_diff
        else:
            total_diff = self.total_budget() - self.total_spending()
            if total_diff < 0:
                print(f"Your current month spending is overbudget by ${total_diff}.")
            return total_diff
