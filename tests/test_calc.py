"""Unit tests for calculation logic in expense-split."""

import copy
import io
import unittest
from contextlib import redirect_stdout
from types import SimpleNamespace
from unittest.mock import patch

from split.calc import split_equally, split_by_share, who_owes, get_net_balances
from split.cli import cmd_settle


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


class TestSettleCommand(unittest.TestCase):

    def setUp(self):
        self.group_data = {
            "members": ["ravi", "priya"],
            "expenses": [
                {"paid_by": "priya", "amount": 400.00, "split": "equal"}
            ],
            "settlements": []
        }

    def test_settle_records_payment_in_debt_direction_and_clears_debt(self):
        group = copy.deepcopy(self.group_data)
        args = SimpleNamespace(group="groupA", payer="ravi", receiver="priya")

        with patch("split.cli.load_group", return_value=group), \
                patch("split.cli.save_group") as save_group, \
                redirect_stdout(io.StringIO()):
            cmd_settle(args)

        save_group.assert_called_once_with("groupA", group)
        self.assertEqual(
            group["settlements"],
            [{"from": "ravi", "to": "priya", "amount": 200.0}]
        )
        self.assertEqual(who_owes(group), [])

    def test_settle_rejects_reverse_direction(self):
        group = copy.deepcopy(self.group_data)
        args = SimpleNamespace(group="groupA", payer="priya", receiver="ravi")
        output = io.StringIO()

        with patch("split.cli.load_group", return_value=group), \
                patch("split.cli.save_group") as save_group, \
                redirect_stdout(output):
            cmd_settle(args)

        save_group.assert_not_called()
        self.assertEqual(group["settlements"], [])
        self.assertEqual(
            who_owes(group),
            [{"from": "ravi", "to": "priya", "amount": 200.0}]
        )
        self.assertIn("No pending debt found between priya and ravi.", output.getvalue())


if __name__ == "__main__":
    unittest.main()
