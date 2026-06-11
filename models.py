import uuid # for giving unique id
from datetime import date

class Task:
    # constructor when new task object is formed
    def __init__(self, name, priority, due_date, status="Pending", created=None, task_id=None):
        self.id = task_id or str(uuid.uuid4()) # for generating id after or 
        self.name = name
        self.priority = priority
        self.due_date = due_date
        self.status = status
        self.created = created or str(date.today())

# converting task object to dictionary , helps for json
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "priority": self.priority,
            "due_date": self.due_date,
            "status": self.status,
            "created": self.created
        }
# to convert dict back into task obj
    @staticmethod
    def from_dict(data):
        return Task(
            name=data["name"],
            priority=data["priority"],
            due_date=data["due_date"],
            status=data["status"],
            created=data["created"],
            task_id=data["id"]
        )