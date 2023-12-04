# Utilities

The sub-package `utilities` serves as the main user interface for `mybudgeter` and acts as a bridge between users and the `database` sub-package. Through this sub-package, users of `mybudgeter` can create a `User` object to access and modify information in the SQLite databases housing their transaction and budget data.

## Features and Usage

The `utilities` sub-package is divided into two modules. The first is `users.py`, which contains the `User` class functioning as the user interface. The second is `helper.py`, containing three helper functions for querying information from the databases for the `User` class.

Users can utilize `mybudgeter` by creating a `User` object with the filenames of both the budget and transaction SQLite databases. If no database filenames are given, the object will create two separate databases in the user's current working directory to store budget and transaction data. The `User` object will then instantiate both `Budget` and `Transactions` class objects from the `database` sub-package, allowing users to interact with the databases using functions under those two classes (e.g., add, modify, delete transaction or budget information in their respective databases).

In addition to connecting users with the `database` sub-package, the `User` class has two other functionalities:

1. Give users the freedom to check simple statistics of their budget and spending data (e.g., calculate the total spending or budget in the listed months, find the highest or lowest spending category).
2. Provide summaries and data visualizations that give users quick access to their spending and budget information.

## Class and Functions

1. **users.py**: the main module of the `utilities` sub-package.
    1. `User`: the main class in `utilities`, containing both `Budget` and `Transactions` class objects that allow users to access functions under those two classes.
        1. `total()`: Takes categories, months, and years as parameters, queries the total spending or budget based on user inputs. The default query is to return the total spending.
        2. `average()`: Takes categories, months, and years as parameters, queries the average spending or budget based on user inputs. The default query is to return the average transaction spending.
        3. `remaining_budget()`: Takes categories, months, and years as parameters, queries the difference between budget and spending based on user inputs, warns the user if the remaining budget becomes negative. The default query is to return the difference between the total budget and total spending.
        4. `highest_spending()`: Takes a boolean value, queries the highest spending category or highest spending month in the current year. The default query is to return the highest spending category and the amount.
        5. `lowest_spending()`: Takes a boolean value, queries the lowest spending category or highest spending month in the current year. The default query is to return the lowest spending category and the amount.
        6. `summary()`: Prints a summary containing information about the user's remaining budget, highest and lowest spending categories and months, and their respective amounts.
        7. `pie_chart()`: Returns a pie chart that breaks down the user's total transaction or budget amount by categories. The default shows the breakdown of total transactions by categories.
        8. `line_chart()`: Returns a line chart showing the user's spending or budget trend over the last 12 months. The default shows the user's spending trend over the last 12 months.

2. **helper.py**: A sub-module that contains functions to help build the SQL query for functions in the `User` class, reducing the amount of repetitive code.
    1. `calculation_query()`: A helper function for `total()` and `average()`, helps build and return the WHERE clause for the SQL query based on user inputs in the respective functions.
    2. `spending_query()`: A helper function for `highest_spending()` and `lowest_spending()`, helps build and return the SQL query based on user inputs in the respective functions.
    3. `linechart_query()`: A helper function for `line_chart()`, helps build and return the SQL query based on user inputs in the function.
