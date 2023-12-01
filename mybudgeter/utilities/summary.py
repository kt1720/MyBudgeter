import matplotlib
from utilities import calculations
class summary():
    def __init__(self, calculator) -> None:
        self.calculator = calculator
    
    def summary(self) -> str:
        remaining_budget = self.calculator.remaining_budget()
        if remaining_budget is not None:
            message = f"Remaining Budget: ${remaining_budget:.2f}\n"
        else:
            message = "Error calculating remaining budget."
        return message