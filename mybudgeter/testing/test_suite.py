import unittest
from budget_test import TestBudget
from transactions_test import TestTransactions

def my_suite():
	suite = unittest.TestSuite
	result = unittest.TestResult()
	# add test for budget
	suite.addTest(TestBudget('test_add_category'))
	suite.addTest(TestBudget('test_modify'))
	suite.addTest(TestBudget('test_delete'))
	suite.addTest(TestBudget('test_check'))
	suite.addTest(TestBudget('test_get_categories'))
	# add test for transactions
	suite.addTest(TestTransactions('test_add_transaction'))
	suite.addTest(TestTransactions('test_modify_transaction'))
	suite.addTest(TestTransactions('test_delete_transaction'))
	suite.addTest(TestTransactions('test_get_n_transactions'))

	runner = unittest.TextTestRunner() 
	print(runner.run(suite))

if __name__ == '__main__':
	my_suite()