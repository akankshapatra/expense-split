"""Command Line Interface for Expense Split."""

import argparse
import sys
from split.calc import split_equally, who_owes, settle_plan
from split.io import load_group, save_group, load_all_groups


def cmd_summary(args):
    group = load_group(args.group)
    if not group:
        print(f"Error: Group '{args.group}' not found.")
        return

    print(f"\nGroup: {group.get('name', args.group)}")
    print(f"Members: {', '.join(group.get('members', []))}")
    print("-" * 50)
    print("Expenses:")
    total = 0.0
    for exp in group.get("expenses", []):
        print(f"  • {exp['description']}: ₹{exp['amount']:.2f} (paid by {exp['paid_by']})")
        total += exp["amount"]
    print(f"\nTotal Group Spend: ₹{total:.2f}")

    print("\nDebts & Dues:")
    debts = who_owes(group)
    if not debts:
        print("  All settled up!")
    else:
        for d in debts:
            print(f"  • {d['from'].capitalize()} owes {d['to'].capitalize()} ₹{d['amount']:.2f}")


def cmd_add_expense(args):
    group = load_group(args.group)
    if not group:
        print(f"Error: Group '{args.group}' not found.")
        return

    amount = float(args.amount)

    expenses = group.get("expenses", [])
    next_id = len(expenses) + 1
    new_expense = {
        "id": next_id,
        "description": args.description,
        "amount": amount,
        "paid_by": args.paid_by.lower(),
        "split": args.split.lower()
    }
    expenses.append(new_expense)
    group["expenses"] = expenses
    save_group(args.group, group)
    print(f"Added expense '{args.description}' of ₹{amount:.2f} to {args.group}.")


def cmd_settle(args):
    group = load_group(args.group)
    if not group:
        print(f"Error: Group '{args.group}' not found.")
        return

    payer = args.payer.lower()
    receiver = args.receiver.lower()
    debts = who_owes(group)

    owed_record = next((d for d in debts if d["from"] == payer and d["to"] == receiver), None)

    if not owed_record:
        print(f"No pending debt found between {args.payer} and {args.receiver}.")
        return

    amount = owed_record["amount"]
    settlements = group.get("settlements", [])
    settlements.append({
        "from": payer,
        "to": receiver,
        "amount": amount
    })
    group["settlements"] = settlements
    save_group(args.group, group)
    print(f"Settled! {args.payer.capitalize()} paid ₹{amount:.2f} to {args.receiver.capitalize()}.")


def cmd_settle_plan(args):
    group = load_group(args.group)
    if not group:
        print(f"Error: Group '{args.group}' not found.")
        return

    payments = settle_plan(group)
    if not payments:
        print("  All settled up!")
    else:
        print("Settle Plan:")
        for p in payments:
            print(f"  • {p['from'].capitalize()} must pay {p['to'].capitalize()} ₹{p['amount']:.2f}")


def main():
    parser = argparse.ArgumentParser(description="Expense Split CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # summary
    p_sum = subparsers.add_parser("summary", help="Show summary and balances for a group")
    p_sum.add_argument("group", help="Group identifier (e.g. groupA, flatmates)")
    p_sum.set_defaults(func=cmd_summary)

    # add-expense
    p_add = subparsers.add_parser("add-expense", help="Add an expense to a group")
    p_add.add_argument("group", help="Group identifier")
    p_add.add_argument("description", help="Expense description")
    p_add.add_argument("amount", type=float, help="Amount paid")
    p_add.add_argument("paid_by", help="Member who paid")
    p_add.add_argument("split", choices=["equal", "share"], default="equal", nargs="?", help="Split type")
    p_add.set_defaults(func=cmd_add_expense)

    # settle
    p_set = subparsers.add_parser("settle", help="Settle debts between members")
    p_set.add_argument("group", help="Group identifier")
    p_set.add_argument("payer", help="Person paying the settlement")
    p_set.add_argument("receiver", help="Person receiving the settlement")
    p_set.set_defaults(func=cmd_settle)

    # settle-plan
    p_plan = subparsers.add_parser("settle-plan", help="Show the smallest list of payments to clear everything")
    p_plan.add_argument("group", help="Group identifier")
    p_plan.set_defaults(func=cmd_settle_plan)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == "__main__":
    main()
