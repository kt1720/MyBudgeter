import sqlite3

class calculator():
    TRANSACTION_TYPE = "transactions"
    BUDGET_TYPE = "budget"

    def __init__(self, budget_db, transaction_db) -> None:
        self.__connect(budget_db, transaction_db)

    def __connect(self, budget, transaction):
        try:
            # Connect to the budget database
            self.__budget_cnx = sqlite3.connect(budget)
            self.budget_cur = self.__budget_cnx.cursor()
            # Connect to the transactions database
            self.__transactions_cnx = sqlite3.connect(transaction)
            self.transactions_cur = self.__transactions_cnx.cursor()
        except sqlite3.Error as e:
            print("Error connecting to databases:", e)
            # Optionally handle the exception here or re-raise it if needed
            self.__close()

    def __close(self):
        self.budget_cur.close()
        self.transactions_cur.close()
        self.__budget_cnx.close()
        self.__transactions_cnx.close()

    def total(self, type=TRANSACTION_TYPE, categories=None, months=None, years=None) -> float:
        """Calculate the total spending or budget."""
        try:
            # Build the base query
            base_query = f"SELECT SUM(amount) FROM {type}"

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
                if isinstance(months, int):
                    months = [months]  # Convert single month to list
                month_placeholders = ', '.join('?' for _ in months)
                conditions.append(f"strftime('%m', trans_date) IN ({month_placeholders})")
                values.extend(str(month).zfill(2) for month in months)

            if years:
                if isinstance(years, int):
                    years = [years]  # Convert single month to list
                year_placeholders = ', '.join('?' for _ in years)
                conditions.append(f"strftime('%Y', trans_date) IN ({year_placeholders})")
                values.extend(str(year).zfill(2) for year in years)

            # Add WHERE clause if conditions are present
            where_clause = " AND ".join(conditions)
            full_query = f"{base_query} WHERE {where_clause}" if where_clause else base_query

            # Execute the query
            getattr(self, f"{type}_cur").execute(full_query, values)

            total = getattr(self, f"{type}_cur").fetchone()[0]
            return total

        except sqlite3.Error as e:
            print("Error calculating total:", e)
            return None

    def remaining_budget(self, categories=None, month=None, year=None) -> float:
        """
        Calculate if the user is over or under budget base on the total in budget and spending.
        Default calculation will be the difference between the subtotal in budget and spending.
        user can choose to calculate the remaining budget for a given category in a specific month and year.
        warn the user if the user is overbudget
        """
        total_budget = self.total("budget", categories, month, year)
        total_transaction = self.total("transactions", categories, month, year)
        if total_budget != None and total_transaction != None:
            remaining_budget = total_budget - total_transaction
            if remaining_budget < 0:
                print(f"Warning: You are over budget by ${abs(remaining_budget)}.")
            return remaining_budget
        else:
            print("Error calculating remining budget.")
            return None
        

    def average(self, type=TRANSACTION_TYPE, categories=None, months=None, years=None) -> float:
        """Calculate the average spending or budget."""
        try:
            # Build the base query
            base_query = f"SELECT AVG(amount) FROM {type}"

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
                if isinstance(months, int):
                    months = [months]  # Convert single month to list
                month_placeholders = ', '.join('?' for _ in months)
                conditions.append(f"strftime('%m', trans_date) IN ({month_placeholders})")
                values.extend(str(month).zfill(2) for month in months)

            if years:
                if isinstance(years, int):
                    years = [years]  # Convert single month to list
                year_placeholders = ', '.join('?' for _ in years)
                conditions.append(f"strftime('%Y', trans_date) IN ({year_placeholders})")
                values.extend(str(year).zfill(2) for year in years)

            # Add WHERE clause if conditions are present
            where_clause = " AND ".join(conditions)
            full_query = f"{base_query} WHERE {where_clause}" if where_clause else base_query

            # Execute the query
            getattr(self, f"{type}_cur").execute(full_query, values)

            average = getattr(self, f"{type}_cur").fetchone()[0]
            return average

        except sqlite3.Error as e:
            print("Error calculating total:", e)
            return None
        
def highest_spending(self, category=True, year=False):
        """
        Find the highest spending based on the provided input.
        - If category is given, find the highest spending in that category.
        - If year is given, find the highest spending month in that year.
        - If neither category nor year is given, find the highest spending year.
        """
        try:
            # Build the base query
            base_query = f"SELECT"

            # Prepare conditions and values for WHERE clause
            conditions = []
            values = []

            if category:
                base_query += f" category, SUM(amount) FROM transactions GROUP BY category"
            elif year:
                base_query += f" strftime('%m', trans_date) as month, SUM(amount) FROM transactions WHERE strftime('%Y', trans_date) = ? GROUP BY month"
                conditions.append("strftime('%Y', trans_date) = ?")
                values.append(str(year))
            else:
                base_query += f" strftime('%Y', trans_date) as year, SUM(amount) FROM transactions GROUP BY year"

            # Add WHERE clause if conditions are present
            where_clause = " AND ".join(conditions) if conditions else ""
            full_query = f"{base_query} {where_clause} ORDER BY SUM(amount) DESC LIMIT 1"

            # Execute the query
            self._spending_cur.execute(full_query, values)

            result = self._spending_cur.fetchone()
            if result:
                highest_spending_value = result[0]
                highest_amount = result[1]
                return f"Highest Spending: {highest_spending_value}, Amount: ${highest_amount:.2f}"
            else:
                return "No data found."

        except sqlite3.Error as e:
            print("Error finding highest spending:", e)
            return None
