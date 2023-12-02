import os
from datetime import datetime
from database.budget import Budget
from database.transactions import Transactions

class User(object):
    TRANSACTION_TYPE = "transactions"
    BUDGET_TYPE = "budget"

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
    
    def calculate(self, type=TRANSACTION_TYPE, operation="total", categories=None, months=None, years=None) -> float:
        """Calculate the total or average spending or budget."""
        # Build the base query
        if operation == "total":
            base_query = f"SELECT SUM(amount) FROM {type}"
        elif operation == "average":
            base_query = f"SELECT AVG(amount) FROM {type}"
        else:
            raise ValueError("Invalid operation. Please use 'total' or 'average'.")

        # Prepare conditions and values for WHERE clause
        conditions = []
        values = []

        if categories:
            if isinstance(categories, str):
                categories = [categories]
            placeholders = ', '.join('?' for _ in categories)
            conditions.append(f"category IN ({placeholders})")
            values.extend(categories)

        if months:
            if not isinstance(months, list):
                months = [months]
            if type == User.TRANSACTION_TYPE:
                month_placeholders = ', '.join('?' for _ in months)
                conditions.append(f"strftime('%m', trans_date) IN ({month_placeholders})")
                values.extend(str(month) for month in months)
            elif type == User.BUDGET_TYPE:
                month_placeholders = ', '.join('?' for _ in months)
                conditions.append(f"month IN ({month_placeholders})")
                values.extend(months)

        if years:
            if not isinstance(years, list):
                years = [years]
            if type == User.TRANSACTION_TYPE:
                year_placeholders = ', '.join('?' for _ in years)
                conditions.append(f"strftime('%Y', trans_date) IN ({year_placeholders})")
                values.extend(str(year) for year in years)
            elif type == User.BUDGET_TYPE:
                year_placeholders = ', '.join('?' for _ in years)
                conditions.append(f"year IN ({year_placeholders})")
                values.extend(years)

        # Add WHERE clause if conditions are present
        where_clause = " AND ".join(conditions)
        full_query = f"{base_query}{' WHERE ' + where_clause if where_clause else ''}"

        # Execute the query
        getattr(self, type).query(query=full_query, args=values)
        result = getattr(self, type).cur.fetchone()[0]
        return result

    def remaining_budget(self, categories=None, month=None, year=None) -> float:
            """
            Calculate if the user is over or under budget base on the total in budget and spending.
            Default calculation will be the difference between the subtotal in budget and spending.
            user can choose to calculate the remaining budget for a given category in a specific month and year.
            warn the user if the user is overbudget
            """
            total_budget = self.calculate("budget", "total", categories, month, year)
            total_transaction = self.calculate("transactions", "total", categories, month, year)
            if total_budget != None and total_transaction != None:
                remaining_budget = total_budget - total_transaction
                if remaining_budget < 0:
                    print(f"Warning: You are over budget by ${abs(remaining_budget)}.")
                return remaining_budget
            else:
                print("Error calculating remining budget.")
                return None

    def highest_spending(self, calculate_category=True):
            """
            Find the highest spending based on the provided input.
            - If calculate_category is True, find the highest spending category in general.
            - If calculate_category is False, find the highest spending month in the current year.
            """
            if calculate_category:
                self.transactions.query("SELECT category, SUM(amount) FROM transactions GROUP BY category ORDER BY SUM(amount) DESC LIMIT 1")
                result = self.transactions.cur.fetchone()
                if result:
                    highest_spending_category, highest_amount = result
                    print(f"Highest spending category: {highest_spending_category}, Amount: ${highest_amount:.2f}")
                    return highest_spending_category, highest_amount
                else:
                    return "No data found for highest spending category."
            else:
                current_year = datetime.now().year
                self.transactions.query("SELECT strftime('%m', trans_date) as month, SUM(amount) FROM transactions WHERE strftime('%Y', trans_date) = ? GROUP BY month ORDER BY SUM(amount) DESC LIMIT 1", (str(current_year),))
                result = self.transactions.cur.fetchone()
                if result:
                    highest_spending_month, highest_amount = result
                    print(f"Highest spending month in current year: {highest_spending_month}, Amount: ${highest_amount:.2f}")
                    return highest_spending_month, highest_amount
                else:
                    return "No data found for highest spending month in the current year."

    def lowest_spending(self, calculate_category=True):
        """
        Find the lowest spending based on the provided input.
        - If calculate_category is True, find the lowest spending category in general.
        - If calculate_category is False, find the lowest spending month in the current year.
        """
    
        if calculate_category:
            self.transactions.query("SELECT category, SUM(amount) FROM transactions GROUP BY category ORDER BY SUM(amount) LIMIT 1")
            result = self.transactions.cur.fetchone()
            if result:
                lowest_spending_category, lowest_amount = result
                print(f"Lowest spending category: {lowest_spending_category}, Amount: ${lowest_amount:.2f}")
                return lowest_spending_category, lowest_amount
            else:
                return "No data found for highest spending category."
        else:
            current_year = datetime.now().year
            self.transactions.query("SELECT strftime('%m', trans_date) as month, SUM(amount) FROM transactions WHERE strftime('%Y', trans_date) = ? GROUP BY month ORDER BY SUM(amount) LIMIT 1", (str(current_year),))
            result = self.transactions.cur.fetchone()
        if result:
            lowest_spending_month, lowest_amount = result
            print(f"Lowest spending month in current year: {lowest_spending_month}, Amount: ${lowest_amount:.2f}")
            return lowest_spending_month, lowest_amount
        else:
            return "No data found for highest spending month in the current year."
