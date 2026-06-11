# TaskPilot

A feature-rich Personal Task Manager built using Python and Tkinter. TaskPilot helps users organize, track, and manage daily tasks efficiently through an interactive graphical user interface.

Originally developed as a Command Line Interface (CLI) application and later upgraded into a full GUI-based desktop application.

## Features

* Add Tasks
* Edit Tasks
* Delete Tasks with Confirmation Popup
* Mark Tasks as Complete
* Toggle Task Status with Double Click
* Search Tasks in Real Time
* Sort Tasks by:

  * Priority
  * Due Date
  * Status
* Clear Completed Tasks
* Task Statistics (Total, Completed, Pending)
* Dark Mode Support
* Keyboard Shortcuts
* Priority-Based Color Coding
* Scrollable Task List
* Persistent JSON Storage

## Technologies Used

* Python
* Tkinter
* CustomTkinter
* JSON
* Object-Oriented Programming (OOP)

## Project Structure

```text
TaskPilot/
│
├── gui.py
├── task_manager_gui.py
├── models.py
├── storage_json.py
├── tasks.json
└── README.md
```

## How to Run

1. Install dependencies:

```bash
pip install customtkinter
```

2. Run the application:

```bash
python gui.py
```

## Keyboard Shortcuts

| Shortcut | Action               |
| -------- | -------------------- |
| Enter    | Add Task             |
| Delete   | Delete Selected Task |
| F2       | Edit Selected Task   |

## Learning Outcomes

Through this project, I learned:

* Object-Oriented Programming
* GUI Development using Tkinter
* Event-Driven Programming
* JSON File Handling
* Data Persistence
* Application Design and Structuring
* User Interface Development

## Future Improvements

* Task Descriptions
* Categories and Tags
* Reminder Notifications
* SQLite Database Integration
* Export Tasks to CSV/PDF
* Cloud Synchronization

## Author

**Shaurya Shukla**

Built as a Python GUI project to practice Object-Oriented Programming, File Handling, and GUI Development.
