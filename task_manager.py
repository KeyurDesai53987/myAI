import json
import datetime

TASK_FILE = "data/tasks.json"

def add_task(task_desc):
    today = str(datetime.date.today())
    try:
        with open(TASK_FILE, 'r') as f:
            tasks = json.load(f)
    except FileNotFoundError:
        tasks = {}

    tasks.setdefault(today, []).append(task_desc)
    with open(TASK_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)
    return "Task added!"

def list_tasks():
    today = str(datetime.date.today())
    try:
        with open(TASK_FILE, 'r') as f:
            tasks = json.load(f)
        return tasks.get(today, [])
    except FileNotFoundError:
        return []
