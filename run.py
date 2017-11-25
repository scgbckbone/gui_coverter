import tkinter as tk
from my_gui import App

root = tk.Tk()
root.title("Console")
App(root).pack(expand=True, fill="both")
root.mainloop()
