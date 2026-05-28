from tkinter import *

root= Tk()
root.title("TASK PILOT")
root.geometry("800x600")
label=Label(root,text="Welcome" , font=("Times New Roman", 25))
label.pack()
text = Text(root, height = 2, width = 30)
text.pack()
button = Button(root, text="Stop", width=25 , font= ("Bold", 14), command=root.destroy)
button.pack()

root.mainloop()