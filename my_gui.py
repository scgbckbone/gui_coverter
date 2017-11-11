import os
import tkinter as tk
from tkinter import Menu
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfilename, asksaveasfilename, asksaveasfile


class App(tk.Frame):

    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)

        self.menu = Menu(master)
        master.config(menu=self.menu)

        self.settings = Menu(self.menu)
        self.menu.add_cascade(label="Settings", menu=self.settings)

        self.console_log = Menu(self.menu)
        self.menu.add_command(label="Log", command=self.save_console_output)

        self.help = Menu(self.menu)
        self.menu.add_cascade(label="HELP", menu=self.help)

        self.text_options = {"state": "disabled",
                             "bg": "black",
                             "fg": "#08c614",
                             "insertbackground": "#08c614",
                             "selectbackground": "#f01c1c"}

        self.text = ScrolledText(self, **self.text_options)
        self.text.pack(expand=True, fill="both")

        self.bottom_in = tk.Frame(self)
        self.prompt = tk.Label(self.bottom_in, text="Choose '.mdb' file: ")
        self.prompt.pack(side="left", fill="x")

        self.bottom_out = tk.Frame(self)
        self.prompt_out = tk.Label(self.bottom_out, text="Choose output file: ")
        self.prompt_out.pack(side="left", fill="x")

        self.entry_in = tk.Entry(self.bottom_in)
        self.entry_in.bind("<Return>", self.choose_file_prompt)
        self.entry_in.bind(
            "<Command-a>",
            lambda e: self.entry_in.select_range(0, "end")
        )
        self.entry_in.bind("<Command-c>", self.clear)
        self.entry_in.focus()
        self.entry_in.pack(side="left", fill="x", expand=True)

        self.entry_out = tk.Entry(self.bottom_out)
        self.entry_out.bind("<Return>", self.choose_file_prompt_out)
        self.entry_out.bind(
            "<Command-a>",
            lambda e: self.entry_out.select_range(0, "end")
        )
        self.entry_out.bind("<Command-c>", self.clear)
        self.entry_out.focus()
        self.entry_out.pack(side="left", fill="x", expand=True)

        self.executer_in = tk.Button(
            self.bottom_in, text="Select", command=self.choose_file
        )
        self.executer_in.pack(side="left", padx=5, pady=2)

        self.clearer_in = tk.Button(
            self.bottom_in, text="Clear", command=self.clear_entry_in
        )
        self.clearer_in.pack(side="left", padx=5, pady=2)

        self.executer_out = tk.Button(
            self.bottom_out, text="Select", command=self.choose_out_file
        )
        self.executer_out.pack(side="left", padx=5, pady=2)

        self.clearer_out = tk.Button(
            self.bottom_out, text="Clear", command=self.clear_entry_out)
        self.clearer_out.pack(side="left", padx=5, pady=2)

        self.bottom_out.pack(side="bottom", fill="both")
        self.bottom_in.pack(side="bottom", fill="both")

    def choose_file(self):
        name = askopenfilename()
        # tkinter.messagebox.showerror('file_name', name)
        if not name:
            return
        self.show("Chosen infile:")
        self.show("\t" + name)

    def choose_out_file(self):
        name = asksaveasfilename(
            filetypes=(("xls files", "*.xls"), ("all files", "*.*"))
        )
        if not name:
            return
        self.show("Outfile will be saved to:")
        self.show("\t" + name)

    def choose_file_prompt(self, event=None):
        file_path = self.entry_in.get()
        if os.path.isfile(file_path):
            file_ = file_path.split(os.sep)[-1].split(".")
            if len(file_) == 2 and file_[1] == "mdb":
                self.show(file_path)
            else:
                self.show_error("Incorrect extension.")
        elif os.path.isdir(file_path):
            self.show_error("Provided path is a directory.")
        else:
            self.show_error("Incorrect file path.")

    def choose_file_prompt_out(self, event=None):
        file_path = self.entry_out.get()
        if os.path.isdir(file_path):
            self.show_error("Provided path is a directory.")
            return
        path_list = file_path.split(os.sep)
        f_name = path_list[-1].split(".")
        if len(f_name) == 2:
            parent_dir = os.sep.join(path_list[:-1])
            if os.path.isdir(parent_dir):
                self.show(file_path)
            else:
                self.show_error("Incorrect file path.")
        else:
            self.show_error("No file extension.")

    def show_error(self, message):
        """Inserts message into the Text wiget"""
        self.text.config(state="normal")
        self.text.insert("end", message + "\n", 'error')
        self.text.tag_config('error', foreground='red')
        self.text.see("end")
        self.text.config(state="disabled")

    def show(self, message):
        """Inserts message into the Text wiget"""
        self.text.config(state="normal")
        self.text.insert("end", message + "\n")
        self.text.see("end")
        self.text.config(state="disabled")

    def clear_entry_in(self):
        """Clears the Entry command widget"""
        self.entry_in.delete(0, "end")

    def clear_entry_out(self):
        """Clears the Entry command widget"""
        self.entry_out.delete(0, "end")

    def clear_text(self):
        """Clears the Text widget"""
        self.text.config(state="normal")
        self.text.delete(1.0, "end-1c")
        self.text.config(state="disabled")

    def clear(self, event=None):
        """Does not stop an eventual running process,
        but just clears the Text and Entry widgets."""
        self.clear_entry_in()
        self.clear_entry_out()
        self.clear_text()

    def save_console_output(self):
        log = self.text.get("1.0", "end-1c")
        file_ = asksaveasfile()
        try:
            file_.write(log)
        except Exception as e:
            self.show_error(e.args)
        finally:
            file_.close()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Console")
    App(root).pack(expand=True, fill="both")
    root.mainloop()