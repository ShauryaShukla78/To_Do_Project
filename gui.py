from tkinter import *
from tkinter import messagebox as msg
from storage_json import save_tasks
from task_manager_gui import TaskManager
from models import Task
import datetime
import customtkinter as ctk

#Initializes TaskManager which handles all task operations (add, delete, update)
manager = TaskManager()
displayed_tasks = []  
search_text = ""
current_sort = "priority"
editing_task_id = None
dark_mode = False

# Refreshes the entire task list in the UI
# Fetches latest tasks from TaskManager and applies sorting + formatting
def show_tasks_gui():
    global displayed_tasks

    task_listbox.delete(0, END)
    displayed_tasks = []

    tasks = manager.get_tasks()

    total_tasks = len(tasks)

    completed_tasks = len([task for task in tasks if task.status.lower() == "done"])

    pending_tasks = total_tasks - completed_tasks

    stats_label.config(
    text=f"Total: {total_tasks} | Completed: {completed_tasks} | Pending: {pending_tasks}"
)

    priority_order = {"high": 0, "medium": 1, "low": 2}

    if current_sort == "priority":
        sorted_tasks = sorted(tasks,key=lambda x: priority_order.get(x.priority.lower(), 3))

    elif current_sort == "date":
        sorted_tasks = sorted(tasks,
        key=lambda x: datetime.datetime.strptime(x.due_date,"%Y-%m-%d"))

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
                break

        save_tasks(manager.tasks)
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

def clear_completed_tasks_gui():

    completed = [task for task in manager.tasks if task.status.lower() == "done"]

    if not completed:
        msg.showinfo(
            "Info",
            "No completed tasks found."
        )
        return
    
    confirm = msg.askyesno(
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

def toggle_theme():
    global dark_mode

    dark_mode = not dark_mode

    if dark_mode:
        root.configure(bg="#2b2b2b")
        main_frame.configure(bg="#2b2b2b")

        left_frame.configure(bg="#3c3f41")
        right_frame.configure(bg="#3c3f41")

        selected_label.configure(bg="#2b2b2b", fg="white")

        taskname_label.configure(bg="#3c3f41", fg="white")
        priority_label.configure(bg="#3c3f41", fg="white")
        duedate_label.configure(bg="#3c3f41", fg="white")

        taskname_entry.configure( bg="#4a4a4a", fg="white", insertbackground="white")

        duedate_entry.configure(bg="#4a4a4a", fg="white", insertbackground="white")

        task_listbox.configure( bg="#4a4a4a", fg="white")

        edit_button.configure( bg="#4a4a4a", fg="white")

        delete_button.configure( bg="#4a4a4a", fg="white")

        complete_button.configure( bg="#4a4a4a", fg="white")

        theme_button.configure( bg="#4a4a4a", fg="white", text="☀️ Light Mode")

        button_frame.configure(bg="#2b2b2b")

        priority_menu.configure( bg="#4a4a4a", fg="white")

        stats_label.configure( bg="#3c3f41", fg="white")

        sort_frame.configure(bg="#3c3f41")

        priority_sort_button.configure( bg="#4a4a4a", fg="white")

        date_sort_button.configure( bg="#4a4a4a", fg="white")

        status_sort_button.configure( bg="#4a4a4a", fg="white")

        clear_completed_button.configure( bg="#4a4a4a", fg="white")

    else:
        root.configure(bg="#f5f6fa")
        main_frame.configure(bg="#f5f6fa")

        left_frame.configure(bg="white")
        right_frame.configure(bg="white")

        selected_label.configure(bg="#f5f6fa", fg="black")

        taskname_label.configure(bg="white", fg="black")
        priority_label.configure(bg="white", fg="black")
        duedate_label.configure(bg="white", fg="black")

        taskname_entry.configure( bg="white", fg="black", insertbackground="black")

        duedate_entry.configure( bg="white", fg="black", insertbackground="black")

        task_listbox.configure( bg="white", fg="black")

        edit_button.configure( bg="SystemButtonFace", fg="black")

        delete_button.configure( bg="SystemButtonFace", fg="black")

        complete_button.configure( bg="SystemButtonFace", fg="black")

        theme_button.configure( bg="SystemButtonFace", fg="black", text="🌙 Dark Mode")

        button_frame.configure(bg="#f5f6fa")

        priority_menu.configure( bg="SystemButtonFace", fg="black")

        stats_label.configure( bg="white", fg="black")

        sort_frame.configure(bg="white")

        priority_sort_button.configure( bg="SystemButtonFace", fg="black")

        date_sort_button.configure( bg="SystemButtonFace", fg="black")

        status_sort_button.configure( bg="SystemButtonFace", fg="black")

        clear_completed_button.configure( bg="SystemButtonFace", fg="black")

# Initializes main Tkinter window and all UI components
root = Tk()
import os , sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

try:
    root.iconbitmap(resource_path("app.ico"))
except Exception as e:
    print("Icon load failed:", e)

root.title("TASK PILOT - Your Personal Task Manager")
root.geometry("900x550")
root.configure(bg="#f5f6fa")

# main frame holds both left (input) and right (task list) sections
main_frame = Frame(root, bg="#f5f6fa")
main_frame.pack(fill=BOTH, expand=True, padx=15, pady=15)

# left frame contains all input fields and add/save button
left_frame = Frame(main_frame, bg="white", padx=20, pady=20, relief=RIDGE, bd=2)
left_frame.pack(side=LEFT, fill=Y)

taskname_label = Label(left_frame, text="Task Name", bg="white")
taskname_label.pack(anchor="w")

taskname_entry = Entry(left_frame, width=30)
taskname_entry.pack(pady=5)


priority_label = Label(left_frame, text="Priority", bg="white")
priority_label.pack(anchor="w")

priority_var = StringVar()
priority_var.set("Low")
priority_menu = OptionMenu(left_frame, priority_var, "High", "Medium", "Low")
priority_menu.pack(fill=X, pady=5)


duedate_label = Label(left_frame, text="Due Date (YYYY-MM-DD)", bg="white")
duedate_label.pack(anchor="w")

duedate_entry = Entry(left_frame, width=30)
duedate_entry.pack(pady=5)

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

stats_label = Label(right_frame,
    text="", bg="white", font=("Arial", 10, "bold")
)
stats_label.pack(pady=(0, 5))

task_listbox = Listbox(right_frame, font=("Arial", 11))
task_listbox.pack(side=LEFT, fill=BOTH, expand=True)
task_listbox.bind("<Double-Button-1>", toggle_task_status)


scrollbar = Scrollbar(right_frame)
scrollbar.pack(side=RIGHT, fill=Y)

task_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=task_listbox.yview)

button_frame = Frame(root, bg="#f5f6fa")
button_frame.pack(pady=10)

edit_button = Button(button_frame, text="Edit", width=12, command=edit_task_gui)
edit_button.grid(row=0, column=0, padx=5)

delete_button = Button(button_frame, text="Delete", width=12, command=delete_task_gui)
delete_button.grid(row=0, column=1, padx=5)

complete_button = Button(button_frame, text="Complete", width=12, command=complete_task_gui)
complete_button.grid(row=0, column=2, padx=5)

theme_button  = Button(button_frame, text="🌙 Dark Mode", width=12, command=toggle_theme
)
theme_button.grid(row=0, column=3, padx=5)

selected_label = Label(root, text="", bg="#f5f6fa", fg="black")
selected_label.pack()

sort_frame = Frame(right_frame, bg="white")
sort_frame.pack(fill=X, pady=(0, 10))

priority_sort_button=Button(sort_frame,text="Priority", width=13,command=sort_by_priority)
priority_sort_button.pack()
date_sort_button=Button(sort_frame,text="Due Date", width=13, command=sort_by_date)
date_sort_button.pack()
status_sort_button=Button(sort_frame,text="Status", width=13, command=sort_by_status)
status_sort_button.pack()
clear_completed_button=Button(sort_frame,text="Clear Completed", width=13,command=clear_completed_tasks_gui
)
clear_completed_button.pack(side=RIGHT, padx=5)


# LOAD + START
show_tasks_gui()
root.bind("<Return>", lambda event: add_task_gui())
root.bind("<Delete>", lambda event: delete_task_gui())
root.mainloop()