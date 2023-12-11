import os
from datetime import datetime, timedelta
import unittest
from mybudgeter.utilities import users, helper

class TestUsers(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> users:
        """Instantiate an User object"""
        cls.user = users.User()

    @classmethod
    def tearDownClass(cls) -> None:
        """Delete the User object and remove the testing databases created in the working directory"""
        del cls.user
        os.remove(os.path.join(os.getcwd(), 'budgeting.db'))
        os.remove(os.path.join(os.getcwd(), 'transactions.db'))
    
    def setUp(self) -> None:
        """Add budget and transaction records to database to test functions in utilities"""
        self.Nov_1 = datetime(2023, 11, 1)
        self.Dec_1_2022 = datetime(2022, 12, 1)
        self.user.budget.add_from_lists(['food', 'clothing', 'school'], [300, 100, 200], [self.Nov_1, self.Dec_1_2022, datetime.now()])
        self.user.transactions.add_transaction('school', 15, name='books')
        self.user.transactions.add_transaction('food', 20, date=self.Nov_1, name='lunch')
        self.user.transactions.add_transaction('food', 25, date=self.Nov_1, name='dinner')
        self.user.transactions.add_transaction('clothing', 30, date=self.Dec_1_2022, name='shirt')
    
    def tearDown(self) -> None:
        """Remove budget and transaction records from the database"""
        self.user.budget.query('DELETE FROM budget')
        self.user.transactions.query('DELETE FROM transactions')
    
    def test_total(self) -> None:
        self.assertEqual(self.user.total(), 90)
        self.assertEqual(self.user.total(categories=["food", "clothing"]), 75)
        self.assertEqual(self.user.total(months=11), 45)
        self.assertEqual(self.user.total(years=2023), 60)
        self.assertEqual(self.user.total(type="budget"), 600)
        self.assertEqual(self.user.total(type="budget", categories=["food", "school"]), 500)
    
    def test_average(self) -> None: 
        self.assertEqual(self.user.average(), 22.5)
        self.assertEqual(self.user.average(categories=["food", "clothing"]), 25)
        self.assertEqual(self.user.average(months=11), 22.5)
        self.assertEqual(self.user.average(years=2023), 20)
        self.assertEqual(self.user.average(type="budget"), 200)
        self.assertEqual(self.user.average(type="budget", categories=["food", "school"]), 250)

    def test_remaining_budget(self) -> None:
        self.assertEqual(self.user.remaining_budget(), 510)
        self.assertEqual(self.user.remaining_budget(categories=["food", "clothing"]), 325)
        self.assertEqual(self.user.remaining_budget(months=11), 255)
        self.assertEqual(self.user.remaining_budget(years=2023), 440)

    def test_highest_spending(self) -> None:
        self.assertEqual(self.user.highest_spending(), ("food", 45))
        self.assertIsNot(self.user.highest_spending(), ("clothing", 30))
        self.assertEqual(self.user.highest_spending(calculate_category=False), ('11', 45))
        self.assertIsNot(self.user.highest_spending(calculate_category=False), ("12", 15))
    
    def test_lowest_spending(self) -> None:
        self.assertEqual(self.user.lowest_spending(), ("school", 15))
        self.assertIsNot(self.user.lowest_spending(), ("clthing", 30))
        self.assertEqual(self.user.lowest_spending(calculate_category=False), ('12', 15))
        self.assertIsNot(self.user.lowest_spending(calculate_category=False), ('11', 45))

    def test_calculation_query(self) -> None:
        self.assertEqual(helper.calculation_query(type="transactions", categories=["food", "clothing"]), ("category IN (?, ?)", ["food", "clothing"]))
        self.assertEqual(helper.calculation_query(type="transactions", categories=["food", "clothing"], months=11, years=2023), ("category IN (?, ?) AND strftime('%m', trans_date) IN (?) AND strftime('%Y', trans_date) IN (?)", ["food", "clothing", '11', '2023']))
        self.assertEqual(helper.calculation_query(type="budget", months=12, years=2023), ("month IN (?) AND year IN (?)", [12, 2023]))
        self.assertEqual(helper.calculation_query(type="budget", categories=["food", "clothing"], months=11, years=2023), ("category IN (?, ?) AND month IN (?) AND year IN (?)", ["food", "clothing", 11, 2023]))

    def test_spending_query(self) -> None:
        self.assertEqual(helper.spending_query(), ("SELECT category, SUM(amount) FROM transactions GROUP BY category ORDER BY SUM(amount) DESC LIMIT 1", ()))
        self.assertEqual(helper.spending_query(order_by="ASC"), ("SELECT category, SUM(amount) FROM transactions GROUP BY category ORDER BY SUM(amount) ASC LIMIT 1", ()))
        self.assertEqual(helper.spending_query(calculate_category=False), ("SELECT strftime('%m', trans_date) as month, SUM(amount) FROM transactions WHERE strftime('%Y', trans_date) = ? GROUP BY month ORDER BY SUM(amount) DESC LIMIT 1", (str(datetime.now().year),)))
        self.assertEqual(helper.spending_query(calculate_category=False, order_by="ASC"), ("SELECT strftime('%m', trans_date) as month, SUM(amount) FROM transactions WHERE strftime('%Y', trans_date) = ? GROUP BY month ORDER BY SUM(amount) ASC LIMIT 1", (str(datetime.now().year),)))

    def test_linechart_query(self) -> None:
        self.assertEqual(helper.linechart_query(type="transactions"), f"SELECT strftime('%Y-%m', trans_date) AS month, SUM(amount) FROM transactions WHERE trans_date BETWEEN '{(datetime.now()-timedelta(days=365)).strftime('%Y-%m-%d')}' AND '{datetime.now().strftime('%Y-%m-%d')}' GROUP BY strftime('%Y-%m', trans_date) ORDER BY month")
        self.assertEqual(helper.linechart_query(type="budget"), f"SELECT printf('%d-%02d', year, month) AS month, SUM(amount) FROM budget WHERE printf('%d-%02d', year, month) BETWEEN '{(datetime.now()-timedelta(days=365)).strftime('%Y-%m-%d')}' AND '{datetime.now().strftime('%Y-%m-%d')}' GROUP BY year, month ORDER BY month")
        self.assertIsNot(helper.linechart_query(type="transactions"), "SELECT strftime('%Y-%m', trans_date) AS month, SUM(amount) FROM transactions WHERE trans_date BETWEEN '2022-12-01' AND '2023-12-01' GROUP BY strftime('%Y-%m', trans_date) ORDER BY month")
        self.assertIsNot(helper.linechart_query(type="budget"), "SELECT strftime('%Y-%m', trans_date) AS month, SUM(amount) FROM budget WHERE trans_date BETWEEN '2022-12-01' AND '2023-12-01' GROUP BY strftime('%Y-%m', trans_date) ORDER BY month")
