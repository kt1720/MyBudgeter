# Test suite

This folder contains the testing code for the `database` and `utilities` sub-packages using the `unittest` framework.

## Test set up

There are three test classes created for the three main modules in the `database` and `utilities` sub-packages.

1. **budget_test.py**: Contains the testing code for the methods in the `budget` module under the `database` sub-package.

2. **transactions_test.py**: Contains the testing code for the methods in the `transactions` module under the `database` sub-package.

3. **user_helper_test.py**: Contains the testing code for the methods in the `users` module under the `utilities` sub-package. The testing code for the `helper` module under the `utilities` sub-package is also included in this test file since it won't be helpful to create a seperate test class for the three helper functions.

## Usage of the test suite

**test_suite.py** is the main interface for all the test classes, user can use this file to test all three classes instead of going into each test class individually. 