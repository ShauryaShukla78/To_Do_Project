from storage_json import load_tasks, save_tasks

class TaskManager:
    def __init__(self):
        self.tasks = load_tasks()

    def add_task(self, task):
        self.tasks.append(task)
        save_tasks(self.tasks)

    def delete_task(self, task_id):
        self.tasks = [t for t in self.tasks if t.id != task_id]
        save_tasks(self.tasks)

    def complete_task(self, task_id):
        for t in self.tasks:
            if t.id == task_id:
                t.status = "Done"
        save_tasks(self.tasks)

    def get_tasks(self):
        return self.tasks
    
    def sort_by_date(self):
        self.tasks.sort(key=lambda task: task.due_date)
        save_tasks(self.tasks)

    def sort_by_priority(self):
        priority_order = {
            "High": 0,
            "Medium": 1,
            "Low": 2
        }

        self.tasks.sort(
            key=lambda task: priority_order.get(task.priority, 3)
        )
        save_tasks(self.tasks)

    def clear_completed_tasks(self):
        self.tasks = [task for task in self.tasks if task.status != "Done"]
        save_tasks(self.tasks)
