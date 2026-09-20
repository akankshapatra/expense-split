"""File I/O operations for groups and expense records."""

import json
from pathlib import Path

DEFAULT_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "groups.json"


def load_all_groups(filepath=DEFAULT_DATA_PATH):
    """Loads all group data from JSON."""
    path = Path(filepath)
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_group(group_id, filepath=DEFAULT_DATA_PATH):
    """Loads data for a specific group. Returns None if group not found."""
    groups = load_all_groups(filepath)
    return groups.get(group_id)


def save_group(group_id, group_data, filepath=DEFAULT_DATA_PATH):
    """Saves or updates a specific group in the JSON store."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    groups = load_all_groups(filepath)
    groups[group_id] = group_data
    with open(path, "w", encoding="utf-8") as f:
        json.dump(groups, f, indent=2)
