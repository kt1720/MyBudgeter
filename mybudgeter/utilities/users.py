import os
import matplotlib.pyplot as plt
from mybudgeter.database.budget import Budget
from mybudgeter.database.transactions import Transactions
from mybudgeter.utilities.helper import calculation_query, spending_query, linechart_query

# Create a user-defined exception to handle SQlite query that returns nothing
class SQliteError(Exception):
    def __init__(self, message) -> None:
        self.message = message

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
    
    def total(self, type=TRANSACTION_TYPE, categories=None, months=None, years=None) -> float:
        """Calculate the total spending or budget."""
        # Build the base query
        try:
            base_query = f"SELECT SUM(amount) FROM {type}"
            where_clause, values = calculation_query(type, categories, months, years)
            full_query = f"{base_query}{' WHERE ' + where_clause if where_clause else ''}"

            # Execute the query
            getattr(self, type).query(query=full_query, args=values)
            total = getattr(self, type).cur.fetchone()[0]
            if not total:
                raise SQliteError("The SQlite query did not return anything, please check if you have entered the correct input parameter.")
            return total
        except (AttributeError, TypeError, SQliteError) as e:
            print(f"Error in querying the total: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error in querying the total: {e}")
            raise 
    
    def average(self, type=TRANSACTION_TYPE, categories=None, months=None, years=None) -> float:
        """Calculate the average spending or budget."""
        # Build the base query
        try:
            base_query = f"SELECT AVG(amount) FROM {type}"
            where_clause, values = calculation_query(type, categories, months, years)
            full_query = f"{base_query}{' WHERE ' + where_clause if where_clause else ''}"

            # Execute the query
            getattr(self, type).query(query=full_query, args=values)
            average = getattr(self, type).cur.fetchone()[0]
            if not average:
                raise SQliteError("The SQlite query did not return anything, please check if you have entered the correct input parameter.")
            return average
        except (AttributeError, TypeError, SQliteError) as e:
            print(f"Error in querying the average: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error in querying the average: {e}")
            raise 

    def remaining_budget(self, categories=None, months=None, years=None) -> float:
            """
            Calculate if the user is over or under budget base on the total in budget and spending.
            Default calculation will be the difference between the subtotal in budget and spending.
            user can choose to calculate the remaining budget for a given category in a specific month and year.
            warn the user if the user is overbudget
            """
            try:
                total_budget = self.total("budget", categories, months, years)
                total_transaction = self.total("transactions", categories, months, years)
                if total_budget != None and total_transaction != None:
                    remaining_budget = total_budget - total_transaction
                    if remaining_budget < 0:
                        print(f"Warning: You are over budget by ${abs(remaining_budget)}.")
                    return remaining_budget
                else:
                    raise SQliteError("The SQlite query did not return anything, please check if you have entered the correct input parameter.")
            except (AttributeError, TypeError, SQliteError) as e:
                print(f"Error in querying the remaining budget: {e}")
            except Exception as e:
                print(f"Unexpected error in querying the remaining budget: {e}")
                raise 

    def highest_spending(self, calculate_category=True):
            """
            Find the highest spending based on the provided input.
            - If calculate_category is True, find the highest spending category in general.
            - If calculate_category is False, find the highest spending month in the current year.
            """
            try:
                query, values = spending_query(calculate_category)
                self.transactions.query(query, values)
                result = self.transactions.cur.fetchone()
                if result:
                    query_type, amount = result
                    # print(f"Highest spending category is {query_type}: ${amount:.2f}") if calculate_category else print(f"Highest spending month in the current year is {query_type}: ${amount:.2f}")
                    return query_type, amount
                else:
                    raise SQliteError("There are no data found in the transactions database.")              
            except SQliteError as e:
                print(f"Error in querying the highest spending: {e}")
                return None
            except Exception as e:
                print(f"Unexpected error in querying the highest spending: {e}")
                raise

    def lowest_spending(self, calculate_category=True):
        """
        Find the lowest spending based on the provided input.
        - If calculate_category is True, find the lowest spending category in general.
        - If calculate_category is False, find the lowest spending month in the current year.
        """
        try:
            query, values = spending_query(calculate_category, "ASC")
            self.transactions.query(query, values)
            result = self.transactions.cur.fetchone()
            if result:
                query_type, amount = result
                # print(f"Lowest spending category is {query_type}: ${amount:.2f}") if calculate_category else print(f"Lowest spending month in the current year is {query_type}: ${amount:.2f}")
                return query_type, amount
            else:
                raise SQliteError("There are no data found in the tranasactions database.")          
        except SQliteError as e:
            print(f"Error in querying the lowest spending: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error in querying the lowest spending: {e}")
            raise

    def summary(self):
        """
        Print out an overview of the user's budget information in a dashboard format.
        """
        remaining_budget = self.remaining_budget()
        highest_category, highest_cat_spending = self.highest_spending()
        lowest_category, lowest_cat_spending = self.lowest_spending()
        highest_month, highest_mo_spending = self.highest_spending(False)
        lowest_month, lowest_mo_spending = self.lowest_spending(False)

        # Print the dashboard
        print("\n===== Budget Summary =====")
        print(f"Remaining Budget: ${remaining_budget:.2f}\n")

        print("Category Breakdown:")
        print(f"Highest Spending Category: {highest_category.capitalize():<20}")
        print(f"Spending: ${highest_cat_spending:.2f}")
        print(f"Lowest Spending Category: {lowest_category.capitalize():<20}")
        print(f"Spending: ${lowest_cat_spending:.2f}\n")

        print("Monthly Breakdown:")
        print(f"Highest Spending Month: {highest_month.capitalize()}")
        print(f"Spending: ${highest_mo_spending:.2f}")
        print(f"Lowest Spending Month: {lowest_month.capitalize()}")
        print(f"Spending: ${lowest_mo_spending:.2f}\n")

        if remaining_budget < 0:
            print(f"Warning: Over budget by ${abs(remaining_budget):.2f}\n")
        else:
            print("You are within budget. Keep it up!\n")
        
    def pie_chart(self, type = TRANSACTION_TYPE):
        """
        Plot a pie chart displaying the budget or spending breakdown by categories.
        """
        query = f"SELECT category, SUM(amount) FROM {type} GROUP BY category"
        getattr(self, type).query(query)
        data = getattr(self, type).cur.fetchall()
        categories = [category[0] for category in data]
        amounts = [amount[1] for amount in data]

        # Create a pie chart
        plt.figure(figsize=(8, 8))
        plt.pie(amounts, labels=None, autopct='%1.1f%%', startangle=140)
        plt.title(f"{type.capitalize()} breakdown by categories")
        plt.legend(categories, title="Categories", loc="center left", bbox_to_anchor=(1, 0.5))
        plt.axis('equal')
        plt.show()

    def line_chart(self, type = TRANSACTION_TYPE):
        """
        Plot a line graph displaying the budget or spending trend.
        """
        getattr(self, type).query(linechart_query(type))
        data = getattr(self, type).cur.fetchall()
        months = [month[0] for month in data]
        amounts = [amount[1] for amount in data]

        # Plot the trend
        plt.figure(figsize=(10, 6))
        plt.plot(months, amounts, marker='o', linestyle='-')
        plt.title("Spending Trend Over the Last 12 Months" if type == "transactions" else f"{type.capitalize()} Trend Over the Last 12 Months")
        plt.xlabel("Month")
        plt.ylabel("Amount")
        plt.grid(True)
        plt.show()


