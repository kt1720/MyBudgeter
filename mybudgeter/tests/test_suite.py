import unittest
from tests.budget_test import TestBudget
from tests.transactions_test import TestTransactions
from tests.user_helper_test import TestUsers

def my_suite():
	suite = unittest.TestSuite()
	# add test for budget
	suite.addTest(unittest.makeSuite(TestBudget))
	# add test for transactions
	suite.addTest(unittest.makeSuite(TestTransactions))
	# add test for users and helper functions
	suite.addTest(unittest.makeSuite(TestUsers))

	runner = unittest.TextTestRunner() 
	print(runner.run(suite))

if __name__ == '__main__':
	my_suite()
