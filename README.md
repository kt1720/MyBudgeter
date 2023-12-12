![Unit test run](https://github.com/kt1720/Data-533-Group-16-project/actions/workflows/python-package.yml/badge.svg)

# MyBudgeter Python Package (Data-533-Group-16-project)

A Python package to create simple household budgets.

## Description

`mybudgeter` is a Python package that allows users to set and check budgets for a number of spending categories they choose. Users will be able to add, modify, and delete individual transactions, categorize their spending and set a budget for each category. If a user's spending is over their set budget, the program will alarm the user. The program will allow users to create a brand new SQLite database to store their spending and budget data if it's the first time using the program or import the data from a SQLite database if it's previously created. Users will also have the option to perform basic budget calculations, read or visualize simple budget summary, and visualize spending vs. budget trends.

[Link to PyPI Project](https://pypi.org/project/mybudgeter/)

## Getting Started

### Installing

* pip install mybudgeter

### Executing program

* import user interface from the library
```
from mybudgeter.utilities.users import User
```
* initialize user with new databases
```
user = User()
```
* initialize user with previous databases
```
user = User(budget = 'path/to/budgeting.db', transactions = 'path/to/transactions.db')
```
* add/modify/delete transactions
```
transaction_id = user.transactions.add_transaction(category, amount, date, name)
user.transactions.modify_transaction(transaction_id, field, value)
user.transactions.delete_transaction(transaction_id)
```
* add/modify/delete budget categories
```
user.budget.add_category(category, limit, date)
user.budget.modify_category(category, limit, month, year)
user.budget.delete_categroy(category, month, year)
```
* get total spend/budget
```
user.total(type, categories, months, years)
```
* get average spending/budget
```
user.average(type, categories, months, years)
```
* get remaining budget
```
user.remaining_budget(categories, months, years)
```
* get highest/lowest spending
```
user.highest_spending(calculate_category)
user.lowest_spending(calculate_category)
```
* get budget/spending summary
```
user.summary()
```
* get budget/spending pie/line charts
``` 
user.pie_chart(type)
user.line_chart(type)
```

## Authors

* Kyle Deng
* Jacob Rosen

## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
