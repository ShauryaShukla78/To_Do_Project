from tkinter import *
from tkinter import messagebox as msg
from task_manager import *
from data import tasks
from storage import *
import datetime

editing_index = None
displayed_tasks = []

def show_tasks_gui():
    global displayed_tasks
    task_listbox.delete(0, END)

    priority_order = {
        "high": 0,
        "medium": 1,
        "low": 2
    }
    displayed_tasks = sorted(tasks, key = lambda task: priority_order.get(task["priority"].lower(), 3))

    for i, task in enumerate(displayed_tasks):

        text = f"[{task['status']}] {task['task_name']} | {task['priority']} | {task['due_date']}"

        if task["status"].lower() == "done":
            text = "✓" + text
            task_listbox.insert(END,text )
            task_listbox.itemconfig(i, fg="gray")
        else:
            task_listbox.insert(END, text)
            if task["priority"].lower() == "high": task_listbox.itemconfig(i, fg="red")

            elif task["priority"].lower() == "medium":
                task_listbox.itemconfig(i, fg="orange")

            else:
                task_listbox.itemconfig(i, fg="green")

def add_task_gui():
    global editing_index

    name = taskname_entry.get()
    if name.strip() == "":
        msg.showwarning("Warning", "Task name cannot be empty")
        return
    priority = priority_var.get()
    due_date = duedate_entry.get()
    if not due_date:
        msg.showwarning("Warning", "Enter Due Date")
        return
    try:
        datetime.datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        msg.showwarning("Warning", "Invalid date format. Use YYYY-MM-DD")
        return
    
    print("editing_index =", editing_index)

    if editing_index is None:
        add_task(name, priority, due_date)
    else:
        tasks[editing_index]["task_name"] = name
        tasks[editing_index]["priority"] = priority
        tasks[editing_index]["due_date"] = due_date

        save_tasks(tasks)
        editing_index = None
        addtask_button.config(text="Add Task")
        selected_label.config(text="")

    taskname_entry.delete(0,END)
    duedate_entry.delete(0,END)
    priority_var.set("Low")

    show_tasks_gui()

def delete_task_gui():
    selected_task_index_tuple = task_listbox.curselection()
    if not selected_task_index_tuple :
        msg.showwarning("Warning", "No task selected")
        return
    
    deletion_success = delete_task(selected_task_index_tuple[0])
    if deletion_success:
        show_tasks_gui()
        selected_label.config(text="")

def complete_task_gui():
    selected_task_index_tuple = task_listbox.curselection()
    if not selected_task_index_tuple :
        msg.showwarning("Warning", "No task selected")
        return
    
    updation_success = complete_task(selected_task_index_tuple[0])
    if updation_success:
        show_tasks_gui()
        selected_label.config(text="")

def edit_task_gui():
    global editing_index
    
    selected_index = task_listbox.curselection()
    if not selected_index :
        msg.showwarning("Warning", "No task selected")
        return
    
    task= tasks[selected_index[0]]
    taskname_entry.delete(0, END)
    taskname_entry.insert(0, task["task_name"])
    priority_var.set(task["priority"])
    duedate_entry.delete(0, END)
    duedate_entry.insert(0, task["due_date"])

    editing_index = selected_index[0]

    addtask_button.config(text="Save Changes")
    selected_label.config(text=f"Editing: {task['task_name']}")

def toggle_task_status(event):
    selected = task_listbox.curselection()

    if not selected:
        return

    index = selected[0]

    task = displayed_tasks[index]

    if task["status"].lower() == "pending":
        task["status"] = "Done"
    else:
        task["status"] = "Pending"

    save_tasks2(tasks)
    show_tasks_gui()

root= Tk()
root.title("TASK PILOT")
root.geometry("800x600")
taskname_label=Label(root,text="Task Name:" , font=("Times New Roman", 25))
taskname_label.pack()

taskname_entry = Entry(root)
taskname_entry.pack()

priority_label = Label(root, text="Priority: " , font=("Times New Roman", 19))
priority_label.pack()
priority_var = StringVar()
priority_var.set("Low")
priority_dropdown = OptionMenu(root,priority_var, "High", "Medium", "Low" )
priority_dropdown.pack()

duedate_label = Label(root, text="Due Date: " , font=("Times New Roman", 19))
duedate_label.pack()
duedate_entry = Entry(root)
duedate_entry.pack()


addtask_button = Button(root, text="Add Task", width=25 , font= ("Bold", 14), command=add_task_gui)
addtask_button.pack()

task_listbox = Listbox(root, width=45, height= 15)
task_listbox.pack()
task_listbox.bind("<ButtonRelease-1>", toggle_task_status)

load_tasks()
show_tasks_gui()

delete_button = Button(root, text = "Delete", width = 25, font= ("Bold", 14), command = delete_task_gui)
delete_button.pack()

completetask_button = Button(root, text="Complete Task", width=25 , font= ("Bold", 14), command=complete_task_gui)
completetask_button.pack()

edittask_button = Button(root, text="Edit Task", width=25 , font= ("Bold", 14), command=edit_task_gui)
edittask_button.pack()

selected_label = Label(root, text="", font=("arial", 12))
selected_label.pack()

root.mainloop()