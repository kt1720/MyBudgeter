import unittest
from budget_test import TestBudget
from transactions_test import TestTransactions

def my_suite():
	suite = unittest.TestSuite
	result = unittest.TestResult()
	# add test for budget
	suite.addTest(unittest.makeSuite(TestBudget))
	# add test for transactions
	suite.addTest(unittest.makeSuite(TestTransactions))

	runner = unittest.TextTestRunner() 
	print(runner.run(suite))

if __name__ == '__main__':
	my_suite()