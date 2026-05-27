import os

if not os.path.exists("tasks.txt"):
    open("tasks.txt", "w").close() # to create an empty file if it doesn't exist and to prevent crash on first run.

tasks=[] #It is more like a todo list; this is a list for many tasks to be done in the form of dictionary.