# Source Start Expense Split

Welcome to the **Source Start Expense Split** repository! We're excited to have you as a contributor to our command-line expense sharing and group balance tracking tool built in Python.

As part of **"Source Start"**, an open-source initiative organized by **CSI-SPIT**, this project gives beginners and intermediate developers a hands-on environment to practice financial logic, balance calculations, CLI ergonomics, and automated testing.

---

## Table of Contents

- [Introduction](#introduction)
- [Key Features](#key-features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [1. Fork the Repository](#1-fork-the-repository)
  - [2. Clone Your Fork](#2-clone-your-fork)
  - [3. Running the CLI](#3-running-the-cli)
- [CLI Commands Reference](#cli-commands-reference)
- [Running Tests](#running-tests)
- [How to Contribute](#how-to-contribute)
  - [Contribution Workflow](#contribution-workflow)
  - [Issue Labels & Difficulty Tiers](#issue-labels--difficulty-tiers)
- [Code of Conduct](#code-of-conduct)
- [License](#license)

---

## Introduction

**Expense Split** is a clean, dependency-free tool designed for college flatmates, hackathon teams, and trip groups to record shared spending, calculate who owes what, and settle dues fairly.

All group data and expense histories are stored in human-readable JSON files in `data/groups.json`. Using straightforward terminal subcommands, users can view group balances, record new expenses with equal or custom proportional splits, and log debt settlements.

---

## Key Features

- 👥 **Multi-Group Tracking**: Maintain separate records for different teams, trips, or flatmates.
- 💵 **Flexible Splitting**: Split expenses equally or by customized share weights.
- ⚖️ **Debt Calculation**: Automatically evaluates dues between group members.
- 🤝 **Settlement Logging**: Record when friends pay each other back to clear dues.
- ⚡ **Zero External Dependencies**: Works out of the box on standard Python 3.8+.
- 🧪 **Unit Test Suite**: Includes automated unit tests using Python's native `unittest` module.

---

## Project Structure

```text
expense-split/
├── README.md               # Project guide and contributor documentation
├── LICENSE                 # MIT License
├── .gitignore              # Standard Python ignores
├── data/
│   └── groups.json         # Storage for groups, members, expenses, and settlements
├── split/
│   ├── __init__.py         # Package initialization
│   ├── __main__.py         # Allows running `python -m split`
│   ├── calc.py             # Math logic for equal splits, shares, and debt balances
│   ├── io.py               # File operations for loading and updating groups
│   └── cli.py              # Command-line interface and subcommand parsers
└── tests/
    ├── __init__.py
    └── test_calc.py        # Automated test cases for calculation logic
```

---

## Getting Started

### Prerequisites

All you need is **Python 3.8+** installed on your system.

Check your Python version:
```bash
python3 --version
```

### 1. Fork the Repository

Click the **Fork** button in the top-right corner of this repository page on GitHub to create your personal copy.

### 2. Clone Your Fork

Clone your newly created fork locally:

```bash
git clone https://github.com/techcsispit/expense-split.git
cd expense-split
```

### 3. Running the CLI

Run the tool as a Python module:

```bash
# View summary and current debts for a group
python3 -m split summary groupA

# Add a shared dinner expense
python3 -m split add-expense groupA "Hackathon Pizza" 1200 priya equal

# Settle a debt between friends
python3 -m split settle groupA ravi priya
```

---

## CLI Commands Reference

| Command | Arguments | Description |
|---|---|---|
| `summary` | `<group>` | Displays members, recorded expenses, and pending debts for a group. |
| `add-expense` | `<group> <description> <amount> <paid_by> [split]` | Adds a new expense to the group. |
| `settle` | `<group> <payer> <receiver>` | Records a debt settlement between two members. |

---

## Running Tests

Unit tests are written using Python's standard `unittest` framework:

```bash
python3 -m unittest discover tests
```

To run a specific test file:
```bash
python3 -m unittest tests/test_calc.py
```

> 💡 **Tip for Contributors:** Always run `python3 -m unittest discover tests` before pushing your branch to ensure your changes don't break existing math.

---

## How to Contribute

We welcome and appreciate contributions from everyone participating in **Source Start**!

### Contribution Workflow

1. **Pick an Issue:** Go to the **Issues** tab to find an open task. Leave a comment expressing your interest to be assigned.
2. **Create a Feature Branch:** Keep your `main` branch clean by creating a dedicated topic branch:
   ```bash
   git checkout -b fix/issue-description
   ```
3. **Make Your Changes:** Edit code cleanly, preserving existing conventions and docstrings.
4. **Test Your Changes:**
   - Run automated tests: `python3 -m unittest discover tests`
   - Test manually in your terminal: `python3 -m split summary groupA`
5. **Commit Your Work:** Write clear, descriptive commit messages:
   ```bash
   git commit -m "fix: improve balance calculation accuracy"
   ```
6. **Push to Your Fork:**
   ```bash
   git push origin fix/issue-description
   ```
7. **Open a Pull Request:** Navigate to your fork on GitHub and submit a Pull Request describing your changes.

### Issue Labels & Difficulty Tiers

- 🔁 `good first issue`: Ideal for beginners and first-time open-source contributors.
- 🐛 `bug`: Fixing mathematical discrepancies, edge cases, or command handling issues.
- ✨ `enhancement`: Introducing new features, graph algorithms, or report visualizers.

> 📌 **Note:** All active tasks and bug reports will be announced in the **[Issues](../../issues)** tab. Check the tab to pick your first issue!

---

## Code of Conduct

This project adheres to a community code of conduct fostering a respectful, inclusive, and welcoming learning environment. Please be supportive in all discussions and pull request reviews.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Organized with ❤️ by <b>CSI-SPIT</b> for <b>Source Start</b>.<br>
  Happy Coding! 💰🚀
</p>
