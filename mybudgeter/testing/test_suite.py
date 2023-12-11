import unittest
import sys
import os
user_home = os.path.expanduser("~")
sys.path.append(os.path.join(user_home, "Library/CloudStorage/OneDrive-UBC/MDS_Block3/DATA-533/Data-533-Group-16-project/mybudgeter"))

from budget_test import TestBudget
from transactions_test import TestTransactions
from user_helper_test import TestUsers

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