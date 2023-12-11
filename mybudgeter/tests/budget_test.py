import unittest
import os
import datetime

from mybudgeter.database.budget import Budget

class TestBudget (unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # sets up a new db in cwd 
        self.budget = Budget()

    @classmethod
    def tearDownClass(self):
        # disconnect from db and remove it from directory 
        del self.budget
        os.remove(os.path.join(os.getcwd(), 'budgeting.db'))

    def setUp(self):
        # initialize table with two values in it to test with
        self.budget.add_from_lists(['food', 'clothing'], [300, 100])
        self.date = datetime.datetime.now()

    def tearDown(self):
        # clear the table to start fresh
        self.budget.query('delete from budget')

    # test add_category
    def test_add_category(self):
        self.budget.add_category('school')
        self.assertIn(('school', self.date.month, self.date.year, 0), self.budget.check_budget())
        self.budget.add_category('health', 150)
        self.assertIn(('health', self.date.month, self.date.year, 150), self.budget.check_budget())
        last_month = self.date.replace(month = self.date.month-1)
        self.budget.add_category('health', 100, last_month)
        self.assertIn(('health', last_month.month, last_month.year, 100), self.budget.check_budget(last_month.month, last_month.year))

    # test modify category
    def test_modify(self):
        self.budget.modify_category('food', 120, self.date.month, self.date.year)
        self.assertIn(('food', self.date.month, self.date.year, 120), self.budget.check_budget())
        self.budget.modify_category('clothing', 300, self.date.month, self.date.year)
        self.assertIn(('clothing', self.date.month, self.date.year, 300), self.budget.check_budget())

    # test delete
    def test_delete(self):
        self.budget.delete_category('food', self.date.month, self.date.year)
        self.assertNotIn(('food', self.date.month, self.date.year, 300), self.budget.check_budget())
        self.budget.delete_category('clothing', self.date.month, self.date.year)
        self.assertNotIn(('clothing', self.date.month, self.date.year, 100), self.budget.check_budget())

    # test check
    def test_check(self):
        self.assertEqual(self.budget.check_budget(), [('food', self.date.month, self.date.year, 300), ('clothing', self.date.month, self.date.year, 100)])
        self.assertEqual(self.budget.check_budget(year=1999), [])
        self.budget.add_category('test', 100, datetime.datetime(1999, 5, 17))
        self.assertEqual(self.budget.check_budget(5, 1999), [('test', 5, 1999, 100)])
        
    # test get
    def test_get_categories(self):
        self.assertEqual(self.budget.get_categories(), ['clothing', 'food'])
        self.budget.add_category('test')
        self.assertEqual(self.budget.get_categories(), ['clothing', 'food', 'test'])
        self.budget.modify_category('test', 10, self.date.month, self.date.year)
        self.assertEqual(self.budget.get_categories(), ['clothing', 'food', 'test'])
        self.budget.delete_category('food', self.date.month, self.date.year)
        self.assertEqual(self.budget.get_categories(), ['clothing', 'test'])