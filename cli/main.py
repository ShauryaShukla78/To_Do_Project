from task_manager import *
from storage import *

# load tasks from file when the program starts so that we can work with existing tasks.
load_tasks()


while True:
    print("=" * 6 + " TO-DO-MENU " + "=" * 6)
    print('''1. Add Task
2. View Tasks
3. Complete Task
4. Delete Task
5. Search Task
6. Filter Tasks
7. Edit Task
8. Sort Task
9. Exit''')
    print("=" * 25 )
    try:
        choice =int(input("\nEnter your choice..."))
        if choice==1:
          name=input("\nEnter task name...").title()

          priority=input("Enter priority(High/Medium/Low)...").capitalize()
          while priority not in ["High", "Medium", "Low"]:
            print("Invalid priority!")
            priority=input("Enter priority(High/Medium/Low)...").capitalize()

          due_date=input("Enter deadline (due date [YYYY-MM-DD]) for the task...")
          try:
            datetime.datetime.strptime(due_date, "%Y-%m-%d")

          except ValueError:
            print("Invalid date format!")
            due_date=input("Enter deadline (due date [YYYY-MM-DD]) for the task...")
          
          add_task(name, priority, due_date)

          print("Task added successfully!")

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
            edit_task()
        elif choice==8:
            sort_tasks()
        elif choice==9:
            print("You exited the program...")
            break
        else:
            print("Invalid choice...Please try again...")
    except Exception as e:
        print("Invalid input. Please enter a number.",e)
