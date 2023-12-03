# Database Package

This package contains the necessary classes to interact with our transactions and budget databases.

### database module

The database module contains our base class `Database` which is inherited by the `Transactions` and `Budget` classes.

The `Database` class is initialized with optional `file_path` and `db` arguments. `db` should be a path to a database file. If this is provided, the class will make a connection to the database. If it is not provided a new database is created either in the `file_path` provided or by default in the current working directory.

The `Database` class has the following methods:

`connect(db)` - used to connect to the db and save the connection as an attribute `self.cnx`. It also sets a cursor attribute `self.cur`.

`close()` - closes the connection to the db.

`__del__()` - closes the connection when the class is deleted.

`query(query, args)` - used to query the SQLite db with a SQL query and optional arguments to the query.

`__create_db(filepath)` - empty method that will be implemented by child classes. Meant to create a new database at the given `file_path`.

`get_categories()` - empty method that will be implemented by child classes. Meant to return all distinct categories in the database. 

### budget module

The budget module contains our `Budget` class which inherits from `Database`. This class is used to interact with our budget database.

It has the following methods:

`add_category(category, limit, date)` - adds a new budget `category` to the table. Default `limit` is zero and default `date` is the current date.

`add_from_lists(cat_list, limit_list, date_list)` - allows user to add budget categories to table in bulk by providing lists of values.

`modify_category(category, value, month, year)` - allows the user to change the budget `value` for a given `category`, `month`, `year`.

`delete_category(category, month, year)` - deletes the budget category from the table.

`check_budget(month, year)` - returns a list of budget categories and values for the given `month` and `year` (default is current month and year).

### transactions module

The transactions module contains our `Transactions` class which inherits from `Database`. This class is used to interact with our transactions database.

It has the following methods:

`add_transaction(category, amount, date, name)` - Adds an individual transaction to the transactions table and returns the transaction id when successful. `date` can be a datetime object or None which defaults to the current date. `name` is an optional string parameter to store info about the transaction more info.

`modify_transaction(id, field, value)` - modifies the `value` of the given `field` in the transactions table for the entry with the given `id`.

`delete_transaction(id)` - deletes the transaction from the table.

`get_n_transactions(n, sort_field, asc)` - returns a list of `n` transactions sorted by the `sort_field` in default descending order.
