from data import tasks
# to save tasks in write mode so that no duplicate tasks would be added.
def save_tasks(tasks):
    with open("tasks.txt","w") as file:
        for task in tasks:
            line=f"{task['task_name']} | {task['priority']} | {task['due_date']} | {task['date_of_creation']} | {task['status']}\n"
            file.write(line)

# to save tasks in append mode so that we can add new tasks without overwriting the existing ones.
def save_tasks2(task):
    with open("tasks.txt","a") as file:
            line=f"{task['task_name']} | {task['priority']} | {task['due_date']} | {task['date_of_creation']} | {task['status']}\n"
            file.write(line)

def load_tasks():
    global tasks
    try:
        with open("tasks.txt","r") as file:
            for line in file:
                parts=line.strip().split(" | ")
                if len(parts)==5:
                    task={
                        "task_name" :parts[0],
                        "priority" :parts[1],
                        "due_date" :parts[2],
                        "tdate_of_creation" :parts[3],
                        "status" :parts[4],
                    }
                    tasks.append(task)
    except FileNotFoundError:
        tasks=[]
