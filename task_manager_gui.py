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