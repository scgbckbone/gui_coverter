from tkinter import *
from tkinter.filedialog import askopenfilename
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText


def choose_file():
    name = askopenfilename()
    # tkinter.messagebox.showerror('file_name', name)
    show(name)


def show(message):
    """Inserts message into the Text wiget"""
    text.config(state="normal")
    text.insert("end", message)
    text.see("end")
    text.config(state="disabled")


root = Tk()
Title = root.title("something")
w = Label(root, text="Hello, world!", foreground="red",font=("Helvetica", 16))
w.pack()

text_options = {"state": "disabled",
                "bg": "black",
                "fg": "#08c614",
                "insertbackground": "#08c614",
                "selectbackground": "#f01c1c"}
text = ScrolledText(root, **text_options)
text.pack(expand=True, fill="both")

menu = Menu(root)
root.config(menu=menu)

file = Menu(menu)

file.add_command(label='Choose', command=choose_file)
file.add_command(label='Exit', command=lambda: exit())

menu.add_cascade(label='File', menu=file)

root.mainloop()
