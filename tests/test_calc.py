"""Unit tests for calculation logic in expense-split."""

import unittest
from split.calc import split_equally, split_by_share, who_owes, get_net_balances


class TestSplitCalculations(unittest.TestCase):

    def test_split_equally_even_division(self):
        """Even division without remainder should divide accurately."""
        res = split_equally(120, 3)
        self.assertEqual(res["each"], 40)

    def test_split_equally_invalid_people(self):
        """Zero or negative number of people should raise ValueError."""
        with self.assertRaises(ValueError):
            split_equally(100, 0)

    def test_split_by_share_basic(self):
        """Splitting by proportional weights should divide correctly."""
        shares = {"alice": 2, "bob": 1}
        res = split_by_share(90, shares)
        self.assertEqual(res["alice"], 60.0)
        self.assertEqual(res["bob"], 30.0)

    def test_who_owes_empty_group(self):
        """An empty group should return no debts."""
        self.assertEqual(who_owes({}), [])

    def test_balances_sum_to_zero(self):
        """Net balances in paise should always sum to exactly 0."""
        group_data = {
            "members": ["alice", "bob", "charlie"],
            "expenses": [
                {"paid_by": "alice", "amount": 10.00, "split": "equal"},
                {"paid_by": "bob", "amount": 3.33, "split": "equal"}
            ],
            "settlements": [
                {"from": "charlie", "to": "alice", "amount": 2.00}
            ]
        }
        balances = get_net_balances(group_data)
        self.assertEqual(sum(balances.values()), 0)


if __name__ == "__main__":
    unittest.main()

from split.calc import who_owes, settle_plan

def test_no_self_debt():
    # Simulate a scenario where Alice pays for a group including herself
    group_data = {
        "members": ["Alice", "Bob"],
        "expenses": [{"paid_by": "Alice", "amount": 100}]
    }
    
    # Test who_owes function
    debts = who_owes(group_data)
    for debt in debts:
        assert debt["from"] != debt["to"], "Bug found: Self-debt detected in who_owes!"

    # Test settle_plan function
    payments = settle_plan(group_data)
    for payment in payments:
        assert payment["from"] != payment["to"], "Bug found: Self-debt detected in settle_plan!"