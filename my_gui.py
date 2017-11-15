import os
import tkinter as tk
from tkinter import Menu, OptionMenu, StringVar
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfilename, asksaveasfilename, asksaveasfile
from mdb_fetcher import DataGetter
from xls_writer import XLSWriter


class App(tk.Frame):
    GETTER = DataGetter
    WRITER = XLSWriter

    def __init__(self, master, *args, **kwargs):
        self.infile = None
        self.outfile = None
        self.table = None

        tk.Frame.__init__(self, master, *args, **kwargs)

        self.menu = Menu(master)
        master.config(menu=self.menu)

        self.settings = Menu(self.menu)
        self.menu.add_cascade(label="Settings", menu=self.settings)

        self.text_options = {"state": "disabled",
                             "bg": "black",
                             "fg": "#08c614",
                             "insertbackground": "#08c614",
                             "selectbackground": "#f01c1c"}

        self.text = ScrolledText(self, **self.text_options)
        self.text.pack(expand=True, fill="both")

        # ======================================================================
        self.top_method = tk.Frame(self)
        self.prompt_method = tk.Label(
            self.top_method, text="Choose conversion method: "
        )
        self.prompt_method.pack(side="left", fill="x")
        option_lst_method = ["method1", "method2"]
        self.drop_var_method = StringVar()
        self.drop_var_method.set(option_lst_method[0])
        self.method_options = OptionMenu(
            self.top_method, self.drop_var_method, *option_lst_method
        )
        self.method_options.pack(expand=True)
        self.top_method.pack(fill="x")
        # ======================================================================
        self.top_table = tk.Frame(self)
        self.prompt_table = tk.Label(
            self.top_table, text="Choose table name: "
        )
        self.prompt_table.pack(side="left", fill="x")

        self.entry_table = tk.Entry(self.top_table)
        self.entry_table.bind("<Return>", self.choose_table)
        self.entry_table.bind(
            "<Command-a>",
            lambda e: self.entry_table.select_range(0, "end")
        )
        self.entry_table.bind("<Command-c>", self.clear)
        self.entry_table.focus()
        self.entry_table.pack(side="left", fill="x", expand=True)

        option_lst_table = ["identifikatory", "unspecified"]
        self.drop_var_table = StringVar()
        self.drop_var_table.set(option_lst_table[0])
        self.table_options = OptionMenu(
            self.top_table, self.drop_var_table, *option_lst_table
        )
        self.table_options.pack(expand=True)
        self.top_table.pack(fill="x")
        # ======================================================================
        self.top_columns = tk.Frame(self)
        self.prompt_columns = tk.Label(
            self.top_columns, text="Choose column names: "
        )
        self.prompt_columns.pack(side="left", fill="x")

        self.entry_columns = tk.Entry(self.top_columns)
        self.entry_columns.bind("<Return>", self.choose_columns)
        self.entry_columns.bind(
            "<Command-a>",
            lambda e: self.entry_columns.select_range(0, "end")
        )
        self.entry_columns.bind("<Command-c>", self.clear)
        self.entry_columns.focus()
        self.entry_columns.pack(side="left", fill="x", expand=True)

        option_lst_columns = ["identifikator,meno_majitela", "unspecified"]
        self.drop_var_columns = StringVar()
        self.drop_var_columns.set(option_lst_columns[0])
        self.column_options = OptionMenu(
            self.top_columns, self.drop_var_columns, *option_lst_columns
        )
        self.column_options.pack(expand=True)
        self.top_columns.pack(fill="x")
        # ======================================================================
        self.top_indexes = tk.Frame(self)
        self.prompt_indexes = tk.Label(
            self.top_indexes, text="Choose index position: "
        )
        self.prompt_indexes.pack(side="left", fill="x")

        self.entry_indexes = tk.Entry(self.top_indexes)
        self.entry_indexes.bind("<Return>", self.choose_indexes)
        self.entry_indexes.bind(
            "<Command-a>",
            lambda e: self.entry_indexes.select_range(0, "end")
        )
        self.entry_indexes.bind("<Command-c>", self.clear)
        self.entry_indexes.focus()
        self.entry_indexes.pack(side="left", fill="x", expand=True)

        option_lst_indexes = ["1,2", "unspecified"]
        self.drop_var_indexes = StringVar()
        self.drop_var_indexes.set(option_lst_indexes[0])
        self.index_option = OptionMenu(
            self.top_indexes, self.drop_var_indexes, *option_lst_indexes
        )
        self.index_option.pack(expand=True)
        self.top_indexes.pack(fill="x")
        # ======================================================================

        self.settings.add_command(label="Exit", command=self.on_exit)

        self.console_log = Menu(self.menu)
        self.menu.add_command(label="Log", command=self.save_console_output)

        self.help = Menu(self.menu)
        self.menu.add_cascade(label="HELP", menu=self.help)

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

        # packing bottom frames

        self.bottom_out.pack(side="bottom", fill="both")
        self.bottom_in.pack(side="bottom", fill="both")

    def choose_file(self):
        name = askopenfilename(
            filetypes=(("mdb files", "*.mdb"), ("all files", "*.*"))
        )
        # tkinter.messagebox.showerror('file_name', name)
        if not name:
            return
        self.infile = name

        try:
            self.update_om_tables()
        except:
            pass

        self.show("Chosen infile:")
        self.show("\t" + name)

    def choose_out_file(self):
        name = asksaveasfilename(
            filetypes=(("xls files", "*.xls"), ("all files", "*.*"))
        )
        if not name:
            return
        self.outfile = name
        self.show("Outfile will be saved to:")
        self.show("\t" + name)

    def choose_file_prompt(self, event=None):
        file_path = self.entry_in.get()
        if not file_path:
            return
        if os.path.isfile(file_path):
            file_ = file_path.split(os.sep)[-1].split(".")
            if len(file_) == 2 and file_[1] == "mdb":
                self.infile = file_path
                self.show("Chosen infile:\n\t{}".format(file_path))
            else:
                self.show_error("Incorrect extension.")
        elif os.path.isdir(file_path):
            self.show_error("Provided path is a directory.")
        else:
            self.show_error("Incorrect file path.")

    def choose_file_prompt_out(self, event=None):
        file_path = self.entry_out.get()
        if not file_path:
            return
        if os.path.isdir(file_path):
            self.show_error("Provided path is a directory.")
            return
        path_list = file_path.split(os.sep)
        f_name = path_list[-1].split(".")
        if len(f_name) == 2:
            if f_name[1] == "xls":
                parent_dir = os.sep.join(path_list[:-1])
                if os.path.isdir(parent_dir):
                    self.outfile = file_path
                    self.show("Outfile will be saved to:\n\t{}".format(file_path))
                else:
                    self.show_error("Incorrect file path.")
            else:
                self.show_error("Incorrect file extension. Use '.xls'")
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
        file_ = asksaveasfile(
            filetypes=(("txt files", "*.txt"), ("all files", "*.*"))
        )
        try:
            file_.write(log)
        except Exception as e:
            self.show_error("Failed to save log. {}".format(e.args))
        else:
            self.show("Log saved to {}".format(file_.name))
        finally:
            file_.close()

    def choose_columns(self):
        pass

    def choose_indexes(self):
        pass

    def choose_table(self, event=None):
        input_table = self.entry_table.get()
        if not input_table:
            input_table = self.drop_var_table
        if not input_table:
            return
        if isinstance(input_table, str):
            try:
                display_str = self.update_om_columns(input_table)
            except Exception as e:
                self.show_error(e.args)
            else:
                self.show("TABLE SCHEME:\n")
                self.show(display_str)
            self.drop_var_table = input_table
            self.show("Chosen table:")
            self.show("\t" + self.drop_var_table)

    def show_whole_selection(self):
        self.show("Infile: {}".format(self.infile))
        self.show("Outfile: {}".format(self.outfile))
        self.show("Table: {}".format(self.table))

    def update_om_tables(self):
        menu = self.table_options['menu']
        new_choices = App.GETTER.show_tables(path=self.infile)

        self.drop_var_table.set(new_choices[0])
        menu.delete(0, 'end')
        for table_name in new_choices:
            menu.add_command(
                label=table_name,
                command=lambda value=table_name: self.drop_var_table.set(value)
            )

    def update_om_columns(self, table_name):
        menu = self.column_options['menu']
        show_str, new_choices = App.GETTER.show_columns(
            path=self.infile,
            table=table_name
        )

        self.drop_var_columns.set(new_choices[0])
        menu.delete(0, 'end')
        for column in new_choices:
            menu.add_command(
                label=column,
                command=lambda value=column: self.drop_var_columns.set(value)
            )
        return show_str

    def on_exit(self):
        # log maybe
        self.quit()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Console")
    App(root).pack(expand=True, fill="both")
    root.mainloop()