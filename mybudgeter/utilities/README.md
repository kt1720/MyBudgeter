# utilities 
The sub-package `utilities` acts as the main user interface of `mybudgeter` and a bridge between users and the `database` sub-package. Through this sub-package, user of `mybudgeter` can create a User object to access and modify information in the sqlite databases that house their transaction and budget data.

## Features and Usage
The `utilities` sub-package is divided into two modules, one is users.py which contains the `User` class that acts as the user interface, and the other is helper.py that contains three helper functions for querying information from the databases to the `User` class.

An user can use `mybudgeter` by creating an `User` object with the file names of both the budget and transaction sqlite databases. If no database file names were given, the object will create two seperate databases in user's current working directory to store the budget and transaction data. Then, the `User` object will instantiate both `Budget` and `Transactions` class objects within the `database` sub-package that allow users to interact with the databases using functions under those two classes (e.g. Add, modify, delete transaction or budget information in its respective database).

In addition to acting as a bridge between users and the `database` sub-package, the `User` class has two other functionalities:

1. Give users the freedom to check simple statistics of their budget and spending data (e.g. calculate the total spending or budget in the listed months, find the highest or lowest spending category). 
2. Provide summary and data visualizations that give users quick access to their spending and budget information.

## Class and Functions

1. users.py: the main module of the `utilities` sub-package.
    1. `User`: the main class in `utilties`, contain both `Budget` and `Transactions` class objects that allow users to access functions under those two classes.
        1. `total()`: Takes in categories, months and years as parameters, quieries the total spending or budget base on user inputs. Default query is to return the total spending.
        2. `average()`: Takes in categories, months and years as parameters, quieries the average spending or budget base on user inputs. Default query is to return the average transaction spending.
        3. `remaining_budget()`: Takes in categories, months and years as parameters, quieries the difference between budget and spending base on user inputs, warns user if remaining budget becomes     
                                 negative. Default query is to return the difference between the total budget and total spending.
        4. `highest_spending()`: Takes in a boolean value, queries the highest spending cateogry or highest spending month in the current year. Default query is to return the highest spending category 
                                 and the amount.
        5. `lowest_spending()`: Takes in a boolean value, queries the lowest spending cateogry or highest spending month in the current year. Default query is to return the lowest spending category and 
                                the amount.
        6. `summary()`: Prints a summary that contains information about user's remaining budget, highest and lowest spending category and months, and their respective amounts. 
        7. `pie_chart()`: Returns a piechart that breaks down user's total transaction or budget amount by categories. Default shows the break down of total transaction by categories.
        8. `line_chart()`: Returns a line chart that shows user's spending or budget trend over the last 12 months. Default shows the user's spending trend over the last 12 months.
2. helper.py: A sub-module that contains functions to help assembling the SQL query for functions in the `User` class, and reduces the amount of repetitive codes in the `User` class.
    1. `calculation_query()`: A helper function for `total()` and `average()`, helps assembling and returns the WHERE clause for the SQL query base on user inputs  
                              in the respective functions.
    2. `spending_query()`: A helper function for `highest_spending()` and `lowest_spending()`, helps assembling and returns the SQL query base on user inputs in the respective functions.
    3. `linechart_query()`: A helper function for `line_chart()`, helps assembling and returns the SQL query base on user inputs in the function.
      




