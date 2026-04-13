import datetime
import json

tasks=[] #It is more like a todo list; this is a list for many tasks to be done in the form of dictionary.

# function to add task
def add_task():
    task_name=input("\nEnter task name...")
    priority=input("Estabilish priority(High/Medium/Low)...").capitalize()
    while True:
        due_date=input("Enter deadline (due date [YYYY-MM-DD]) for the task...")
        try:
            datetime.datetime.strptime(due_date, "%Y-%m-%d") #String parse time, it converts string into date object
            break
        except:
            print("Invalid format.")
    created_date=datetime.date.today()
    status="Pending"
    created_date=str(created_date) # to convert date object to string for json file.
    task={
          "task_name":task_name,
          "priority":priority,
          "due_date":due_date,
          "date_of_creation":created_date,
          "status":status
          }# this is a dictionary for a particular task to be entered by the user
    
    tasks.append(task)
    print("Task added successfully!")
    save_tasks(tasks) # to save tasks in json file after adding new tasks
    print("_"*40)

def display(task):
    print(f"Name: {task['task_name']}")
    print(f"Priority: {task['priority']}")
    print(f"Status: {task['status']}")
    print(f"Due Date: {task['due_date']}")
    print(f"Created Date: {task['date_of_creation']}")

    d_date=datetime.datetime.strptime(task['due_date'], "%Y-%m-%d").date()
    cur_date=datetime.date.today()
    days_remaining=(d_date-cur_date).days

    if days_remaining >0:
        print(f"Days Left: {days_remaining} !")
    elif days_remaining==0:
        print("Due today!")
    else:
        print(f"Overdue by {abs(days_remaining)} days.")

# function to view how many tasks were added , they are pending or done ,date of creation and the deadline.
def view_tasks():
    if len(tasks)==0:
        print("No tasks to show...")
        return
    for ind,task in enumerate(tasks,start=1):
        print("\nTask",ind,end="\n\n")
        # for key,value in task.items():
        #     print(f"{key}:{value}")
        display(task)
    print("_"*40)

# function to checklist the tasks that are completed.
def complete_task():
    if len(tasks)==0:
        print("No task to update...")
        return
    view_tasks()
    try:
        task_num=int(input("Enter task number to mark as complete..."))
        if task_num < 1 or task_num > len(tasks):
            print("Exceeded the number of tasks...")
            return
        for idx,task in enumerate(tasks,start=1): 
            if idx==task_num:
                task["status"]="Done"
                print("Task marked as completed...")
                view_tasks()
                break
    except Exception as e:
        print("Invalid input. Please enter a number.",e)
    save_tasks()
    print("_"*40)

def delete_task():
    if len(tasks)==0:
        print("Nothing to be deleted...:(")
        return
    view_tasks()
    while True:
        try:
            del_task=int(input("Enter task number to delete..."))
            if del_task>len(tasks) or del_task<1:
                print("Exceeded (or invalid ) the number of tasks...")
                return
            
            del(tasks[del_task-1])
            save_tasks(tasks)
            print("Task deleted successfully...:)")
            view_tasks()
            break
        except Exception as e:
            print("Invalid input. Please enter a number.",e) 
    print("_"*40)

def save_tasks(tasks):
    with open("tasks.json","w") as json_file:
        json.dump(tasks,json_file,indent=4)

def load_tasks():
    global tasks
    try:
        with open("tasks.json","r") as json_file:
            tasks=json.load(json_file)
    except :
        tasks=[]

def search_task():
    if len(tasks)==0:
        print("Nothing to search...:( ")
        return
    found=False
    count=0
    while True:
        key=input("Enter keyword to search in task names...").lower() # to make search case-insensitive
        for task in tasks:
            if key in task["task_name"].lower():
                count+=1
                print("\n" + "-" * 40)
                print("Matching Task Found")
                display(task)
            found=True

        if found:
            print(f"\nFound {count} task(s) matching the keyword.")
            break
        if not found:
            print("\nNot found!! \nTry another keyword...")
        print("-"*40)

def filter_tasks():
    if len(tasks)==0:
        print("Nothing to filter!")
        return
    found=False
    try:
        while True:
            print("\nFilter by:\n1. Priority\n2. Status\n3. Due Date\n4. Exit")

            choice=input("Enter your choice: ")

            if choice=='1':
                while True:
                    print("\n" + "-" * 40)
                    priority=input("How to filter? (High/Medium/Low/1. (for Exit)): ")
                    if priority=='1':
                        break
                    for task in tasks:
                        if priority.lower()==task["priority"].lower():
                            found=True
                            print("\n" + "-" * 40)
                            display(task)
                    if not found:
                        print("Not found with this priority! ")
                   

            elif choice=='2':
                status=input("How to filter? (Pending/Done): ")
                for task in tasks:
                    if status.lower()==task["status"].lower():
                        found=True
                        print("\n" + "-" * 40)
                        display(task)
                if not found:
                    print("Not found with this status! ")

            elif choice=='3':
                duedate=input("Enter due date to filter (DD-MM-YYYY): ")
                for task in tasks:
                    if duedate==task["due_date"]:
                        found=True
                        print("\n" + "-" * 40)
                        display(task)
                if not found:
                    print("Not found with this due date! ")

            elif choice=='4':
                print("Exiting filter menu.")
                break
        
            else:
                print("Invalid choice!")
        if not found:
            print("Nothing found matching the filter criteria!")
        print("-"*40)
    except Exception as e:
        print(e)

load_tasks()

while True:
    print("=" * 6 + " TO-DO-MENU " + "=" * 6)
    print('''1. Add Task
2. View Tasks
3. Complete Task
4. Delete Task
5. Search Task
6. Filter Tasks
7. Exit''')
    print("=" * 25 )
    try:
        choice =int(input("\nEnter your choice..."))
        if choice==1:
          add_task()
        elif choice==2:
            view_tasks()
        elif choice==3:
            complete_task()
        elif choice==4:
            delete_task()
        elif choice==5:
            search_task()
        elif choice==6:
            filter_tasks()
        elif choice==7:
            print("You exited the program...")
            break
        else:
            print("Invalid choice...Please try again...")
    except Exception as e:
        print("Invalid input. Please enter a number.",e)

