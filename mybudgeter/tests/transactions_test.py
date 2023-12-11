import unittest
import os
import datetime

from mybudgeter.database.transactions import Transactions

class TestTransactions(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # sets up a new db in cwd 
        self.trans = Transactions()

    @classmethod
    def tearDownClass(self):
        # disconnect from db and remove it from directory 
        del self.trans
        os.remove(os.path.join(os.getcwd(), 'transactions.db'))

    def setUp(self):
        # initialize table with transactions in it to test with
        self.dec_1 = datetime.datetime(2023, 12, 1)
        t1 = self.trans.add_transaction('school', 15, name='books')
        t2 = self.trans.add_transaction('food',10, date=self.dec_1, name='lunch')
        t3 = self.trans.add_transaction('food', 20, date=self.dec_1, name='dinner')
        t4 = self.trans.add_transaction('clothing', 30, name='shirt')
        self.date = datetime.datetime.now()
        self.trans_list = [t1, t2, t3, t4]

    def tearDown(self):
        # clear the table to start fresh
        self.trans.query('delete from transactions')
    
    def test_add_transaction(self):
        id1 = self.trans.add_transaction('food', 30)
        self.assertIn((id1, self.date.strftime("%Y-%m-%d"), None, 'food', 30), self.trans.get_n_transactions(5))
        id2 = self.trans.add_transaction('school', 5, self.dec_1)
        self.assertIn((id2, self.dec_1.strftime("%Y-%m-%d"), None, 'school', 5), self.trans.get_n_transactions(6))
        id3 = self.trans.add_transaction('test', 5, self.dec_1, 'testing a name')
        self.assertIn((id3, self.dec_1.strftime("%Y-%m-%d"), 'testing a name', 'test', 5), self.trans.get_n_transactions(7))

    def test_modify_transaction(self):
        self.trans.modify_transaction(self.trans_list[0], 'amount', 100)
        self.assertIn((self.trans_list[0], self.date.strftime("%Y-%m-%d"), 'books', 'school', 100), self.trans.get_n_transactions(4))
        self.trans.modify_transaction(self.trans_list[3], 'trans_date', '2000-12-2')
        self.assertIn((self.trans_list[3], '2000-12-2', 'shirt', 'clothing', 30), self.trans.get_n_transactions(4))
        self.trans.modify_transaction(self.trans_list[1], 'category', 'shopping')
        self.assertIn((self.trans_list[1], self.dec_1.strftime("%Y-%m-%d"), 'lunch', 'shopping', 10), self.trans.get_n_transactions(4))
        self.trans.modify_transaction(self.trans_list[2], 'name', 'breakfast')
        self.assertIn((self.trans_list[2], self.dec_1.strftime("%Y-%m-%d"), 'breakfast', 'food', 20), self.trans.get_n_transactions(4))

    def test_delete_transaction(self):
        self.trans.delete_transaction(self.trans_list[0])
        self.assertNotIn((self.trans_list[0], self.date.strftime("%Y-%m-%d"), 'books', 'school', 15), self.trans.get_n_transactions(4))
        self.assertEqual(len(self.trans.get_n_transactions(4)), 3)
        self.trans.delete_transaction(self.trans_list[3])
        self.assertNotIn((self.trans_list[3], self.date.strftime("%Y-%m-%d"), 'shirt', 'clothing', 30), self.trans.get_n_transactions(4))
        self.assertEqual(len(self.trans.get_n_transactions(4)), 2)

    def test_get_n_transactions(self):
        self.assertEqual(self.trans.get_n_transactions(1), [(self.trans_list[0], self.date.strftime("%Y-%m-%d"), 'books', 'school', 15)])
        self.assertEqual(self.trans.get_n_transactions(1, asc=True), [(self.trans_list[1], self.dec_1.strftime("%Y-%m-%d"), 'lunch', 'food', 10)])
        list1 = [(self.trans_list[3], self.date.strftime("%Y-%m-%d"), 'shirt', 'clothing', 30), (self.trans_list[2], self.dec_1.strftime("%Y-%m-%d"), 'dinner', 'food', 20)]
        self.assertEqual(self.trans.get_n_transactions(2, sort_field="amount", asc=False), list1)
