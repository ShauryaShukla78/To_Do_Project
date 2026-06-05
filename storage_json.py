import json
from models import Task

FILE = "tasks.json"


def save_tasks(tasks):
    with open(FILE, "w") as f:
        json.dump([t.to_dict() for t in tasks], f, indent=4)


def load_tasks():
    try:
        with open(FILE, "r") as f:
            data = json.load(f)
            return [Task.from_dict(t) for t in data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []