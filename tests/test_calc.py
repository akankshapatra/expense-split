"""Unit tests for calculation logic in expense-split."""

import unittest
from split.calc import split_equally, split_by_share, who_owes


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


if __name__ == "__main__":
    unittest.main()
