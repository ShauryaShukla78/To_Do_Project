from tkinter import *
from task_manager import *
from data import tasks
from storage import *

def clicked():
    name = taskname_entry.get()
    priority = priority_var.get()
    due_date = duedate_entry.get()
    if not name or not due_date:
        return
    try:
        datetime.datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD")
        return
    
    add_task(name, priority, due_date)

    taskname_entry.delete(0,END)
    duedate_entry.delete(0,END)
    priority_var.set("Low")
    show_tasks_gui()

def show_tasks_gui():
    task_listbox.delete(0, END)
    for task in tasks:
        task_listbox.insert(END, f"[{task['status']}] {task['task_name']}")

def delete_task_gui():
    selected_task_index_tuple = task_listbox.curselection()
    if not selected_task_index_tuple :
        print("No task selected")
        return
    
    deletion_success = delete_task(selected_task_index_tuple[0])
    if deletion_success:
        show_tasks_gui()

def complete_task_gui():
    selected_task_index_tuple = task_listbox.curselection()
    if not selected_task_index_tuple :
        print("No task selected")
        return
    
    updation_success = complete_task(selected_task_index_tuple[0])
    if updation_success:
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


addtask_button = Button(root, text="Add Task", width=25 , font= ("Bold", 14), command=clicked)
addtask_button.pack()

task_listbox = Listbox(root, width=45, height= 15)
task_listbox.pack()

load_tasks()
show_tasks_gui()

delete_button = Button(root, text = "Delete", width = 25, font= ("Bold", 14), command = delete_task_gui)
delete_button.pack()

completetask_button = Button(root, text="Complete Task", width=25 , font= ("Bold", 14), command=complete_task_gui)
completetask_button.pack()


root.mainloop()