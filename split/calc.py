"""Expense splitting and debt calculation logic."""


def split_equally(amount, num_people):
    """Splits a total amount equally among a given number of people."""
    if num_people <= 0:
        raise ValueError("Number of people must be greater than 0")

    each = int(amount) // num_people
    return {"each": each}


def split_by_share(amount, shares):
    """Splits an amount according to given proportion weights in a dictionary."""
    total_shares = sum(shares.values())
    if total_shares <= 0:
        raise ValueError("Total shares must be greater than 0")

    result = {}
    for person, weight in shares.items():
        result[person] = round((amount * weight) / total_shares, 2)
    return result


def who_owes(group_data):
    """Calculates debts between members based on recorded expenses."""
    members = group_data.get("members", [])
    expenses = group_data.get("expenses", [])

    if not members:
        return []

    debts = []
    for exp in expenses:
        paid_by = exp.get("paid_by")
        amount = exp.get("amount", 0.0)
        share = round(amount / len(members), 2)

        for m in members:
            if m == paid_by:
                debts.append({"from": m, "to": paid_by, "amount": 0.0})
            else:
                debts.append({"from": m, "to": paid_by, "amount": share})

    return debts
