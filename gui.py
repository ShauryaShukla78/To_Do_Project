from tkinter import *
from tkinter import messagebox as msg
from storage_json import load_tasks, save_tasks
from task_manager_gui import TaskManager
from models import Task
import datetime
import customtkinter as ctk
from tkinter import messagebox

#Initializes TaskManager which handles all task operations (add, delete, update)
manager = TaskManager()
displayed_tasks = []  
search_text = ""
current_sort = "priority"
editing_task_id = None

# Refreshes the entire task list in the UI
# Fetches latest tasks from TaskManager and applies sorting + formatting
def show_tasks_gui():
    global displayed_tasks

    task_listbox.delete(0, END)
    displayed_tasks = []

    tasks = manager.get_tasks()

    priority_order = {"high": 0, "medium": 1, "low": 2}

    if current_sort == "priority":
        sorted_tasks = sorted(tasks,key=lambda x: priority_order.get(x.priority.lower(), 3))

    elif current_sort == "date":
        sorted_tasks = sorted(tasks,
        key=lambda x: x.due_date)

    elif current_sort == "status":
        sorted_tasks = sorted(
        tasks,
        key=lambda x: x.status.lower())

    else:
        sorted_tasks = tasks

    if search_text:
            sorted_tasks = [x for x in sorted_tasks if search_text in x.name.lower()]

    for task in sorted_tasks:
        displayed_tasks.append((task.id, task))

        text = f"[{task.status}] {task.name} | {task.priority} | {task.due_date}"

        if task.status.lower() == "done":
            text = "✓ " + text
            task_listbox.insert(END, text)
            task_listbox.itemconfig(END, fg="gray")

        else:
            task_listbox.insert(END, text)

            if task.priority.lower() == "high":
                task_listbox.itemconfig(END, fg="red")
            elif task.priority.lower() == "medium":
                task_listbox.itemconfig(END, fg="orange")
            else:
                task_listbox.itemconfig(END, fg="green")

# Handles both adding new tasks and updating existing ones
def add_task_gui():
    global editing_task_id

    name = taskname_entry.get().strip()
    if not name:
        msg.showwarning("Warning", "Task name cannot be empty")
        return

    priority = priority_var.get()
    due_date = duedate_entry.get().strip()

    if not due_date:
        msg.showwarning("Warning", "Enter Due Date")
        return

    try:
        datetime.datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        msg.showwarning("Warning", "Invalid date format (YYYY-MM-DD)")
        return

    if editing_task_id is None:
        task = Task(name, priority, due_date)
        manager.add_task(task)
    else:
        for t in manager.tasks:
            if t.id == editing_task_id:
                t.name = name
                t.priority = priority
                t.due_date = due_date

        manager._save()
        editing_task_id = None
        addtask_button.config(text="Add Task")
        selected_label.config(text="")

    clear_inputs()
    show_tasks_gui()

# Deletes the selected task from the system
def delete_task_gui():
    selected = task_listbox.curselection()
    if not selected:
        msg.showwarning("Warning", "No task selected")
        return
    confirm = msg.askyesno("Confirm Delete", "Are you sure you want to delete this task?")

    if not confirm:
        return
    
    index = selected[0]
    task_id = displayed_tasks[index][0]

    manager.delete_task(task_id)
    
    selected_label.config(text="")
    show_tasks_gui()

# Marks the selected task as completed/ Done
def complete_task_gui():
    selected = task_listbox.curselection()
    if not selected:
        msg.showwarning("Warning", "No task selected")
        return

    index = selected[0]
    task_id = displayed_tasks[index][0]

    manager.complete_task(task_id)

    selected_label.config(text="")
    show_tasks_gui()

# Loads selected task data into input fields for editing
def edit_task_gui():
    global editing_task_id

    selected = task_listbox.curselection()
    if not selected:
        msg.showwarning("Warning", "No task selected")
        return

    index = selected[0]
    task = displayed_tasks[index][1]

    taskname_entry.delete(0, END)
    taskname_entry.insert(0, task.name)

    priority_var.set(task.priority)
    duedate_entry.delete(0, END)
    duedate_entry.insert(0, task.due_date)

    editing_task_id = task.id

    addtask_button.config(text="Save Changes")
    selected_label.config(text=f"Editing: {task.name}")

# Toggles task status between Pending and Done on list click
def toggle_task_status(event):
    selected = task_listbox.curselection()
    if not selected:
        return

    index = selected[0]
    task_id, task = displayed_tasks[index]

    task.status = "Done" if task.status.lower() == "pending" else "Pending"

    save_tasks(manager.tasks)
    show_tasks_gui()

# Clears all input fields after task submission or update
def clear_inputs():
    taskname_entry.delete(0, END)
    duedate_entry.delete(0, END)
    priority_var.set("Low")

def search_tasks():
    global search_text
    search_text = search_entry.get().lower()
    show_tasks_gui()

def sort_by_date():
    global current_sort
    current_sort = "date"
    show_tasks_gui()

def clear_completed_tasks():

    completed = [task for task in manager.tasks if task.status.lower() == "done"]

    if not completed:
        messagebox.showinfo(
            "Info",
            "No completed tasks found."
        )
        return
    
    confirm = messagebox.askyesno(
        "Confirm",
        f"Delete {len(completed)} completed task(s)?"
    )
    if not confirm:
        return

    manager.tasks = [
        task for task in manager.tasks
        if task.status.lower() != "done"
    ]
    save_tasks(manager.tasks)
    show_tasks_gui()

def sort_by_priority():
    global current_sort
    current_sort = "priority"
    show_tasks_gui()

def sort_by_status():
    global current_sort
    current_sort = "status"
    show_tasks_gui()

# Initializes main Tkinter window and all UI components
root = Tk()
root.title("TASK PILOT - Your Personal Task Manager")
root.geometry("900x550")
root.configure(bg="#f5f6fa")

# main frame holds both left (input) and right (task list) sections
main_frame = Frame(root, bg="#f5f6fa")
main_frame.pack(fill=BOTH, expand=True, padx=15, pady=15)

# left frame contains all input fields and add/save button
left_frame = Frame(main_frame, bg="white", padx=20, pady=20, relief=RIDGE, bd=2)
left_frame.pack(side=LEFT, fill=Y)

Label(left_frame, text="Task Name", bg="white").pack(anchor="w")
taskname_entry = Entry(left_frame, width=30)
taskname_entry.pack(pady=5)


Label(left_frame, text="Priority", bg="white").pack(anchor="w")
priority_var = StringVar()
priority_var.set("Low")
OptionMenu(left_frame, priority_var, "High", "Medium", "Low").pack(fill=X, pady=5)


Label(left_frame, text="Due Date (YYYY-MM-DD)", bg="white").pack(anchor="w")
duedate_entry = Entry(left_frame, width=30)
duedate_entry.pack(pady=5)


addtask_button = Button(root, text="Add Task", width=25, command=add_task_gui)
addtask_button.pack()


addtask_button = Button(
    left_frame,
    text="Add Task",
    bg="#4CAF50",
    fg="white",
    padx=10,
    pady=5,
    command=add_task_gui
)
addtask_button.pack(pady=10, fill=X)

# right frame contains the listbox which displays all tasks and a scrollbar
right_frame = Frame(main_frame, bg="white", padx=10, pady=10, relief=RIDGE, bd=2)
right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

search_entry = ctk.CTkEntry(right_frame, font=("Arial", 12),placeholder_text="Search tasks...")
search_entry.pack(fill=X, pady=5)

search_entry.bind("<KeyRelease>", lambda event: search_tasks())

task_listbox = Listbox(right_frame, font=("Arial", 11))
task_listbox.pack(side=LEFT, fill=BOTH, expand=True)
task_listbox.bind("<Double-Button-1>", toggle_task_status)


scrollbar = Scrollbar(right_frame)
scrollbar.pack(side=RIGHT, fill=Y)

task_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=task_listbox.yview)

button_frame = Frame(root, bg="#f5f6fa")
button_frame.pack(pady=10)

Button(button_frame, text="Edit", width=12, command=edit_task_gui).grid(row=0, column=0, padx=5)
Button(button_frame, text="Delete", width=12, command=delete_task_gui).grid(row=0, column=1, padx=5)
Button(button_frame, text="Complete", width=12, command=complete_task_gui).grid(row=0, column=2, padx=5)


selected_label = Label(root, text="", bg="#f5f6fa", fg="black")
selected_label.pack()

sort_frame = Frame(right_frame, bg="white")
sort_frame.pack(fill=X, pady=(0, 10))

Button(sort_frame,text="Priority", width=13,command=sort_by_priority).pack()
Button(sort_frame,text="Due Date", width=13, command=sort_by_date).pack()
Button(sort_frame,text="Status", width=13, command=sort_by_status).pack()
Button(sort_frame,text="Clear Completed", width=13,command=clear_completed_tasks
).pack(side=RIGHT, padx=5)

# LOAD + START
show_tasks_gui()
root.mainloop()