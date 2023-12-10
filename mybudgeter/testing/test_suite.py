import unittest
from budget_test import TestBudget


def my_suite(): 
	suite = unittest.TestSuite()
	result = unittest.TestResult()
	# add tests for budget
	suite.addTest(TestBudget('test_add_category'))
	suite.addTest(TestBudget('test_modify'))
	suite.addTest(TestBudget('test_delete'))
	suite.addTest(TestBudget('test_check'))
	suite.addTest(TestBudget('test_get_categories'))

	# add tests for transactions
	

	runner = unittest.TextTestRunner() 
	print(runner.run(suite))

if __name__ == '__main__':
	my_suite()