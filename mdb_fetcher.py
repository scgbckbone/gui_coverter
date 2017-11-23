import os
import sys
import pypyodbc
from meza import io
import subprocess


here_path = os.path.abspath(__file__)
here_path = os.sep.join(here_path.split(os.sep)[:-1])


class InvalidInputError(Exception):
    """When both indexes and columns are not specified."""


class DataGetter(object):
    def __init__(self, db_path, table_name, hex_num, name, conversion_method=0):
        self.db_path = db_path
        self.table = table_name
        self.column1 = hex_num
        self.column2 = name
        self.conversion_method = conversion_method
        self.converter = self.choose_converter()
        self.data = None
        self.result = None

    @property
    def is_windows(self):
        if sys.platform == "win32" or sys.platform == "win64":
            return True
        return False

    @property
    def columns(self):
        return self.column1 + "," + self.column2

    @staticmethod
    def is_linux():
        if sys.platform == "linux" or sys.platform == "linux2":
            return True
        return False

    @classmethod
    def show_tables_linux(cls, path):
        tables = subprocess.check_output(["mdb-tables", path])
        return tables.decode().split()

    @classmethod
    def show_columns_linux(cls, path, table):
        column_str = next(io.read_mdb(path, table=table))
        keys = list(column_str.keys())
        column_str = "\n".join(
            [
                "\t{}".format(k)for k in column_str
            ]
        )
        return column_str, keys

    @classmethod
    def show_tables_win(cls, path):
        tables = []
        conn = pypyodbc.win_connect_mdb(path)
        c = conn.cursor()
        try:
            table_objs = c.tables().fetchall()
        except Exception as e:
            # log something
            pass
        else:
            for i in table_objs:
                if i[3] == "TABLE":
                    tables.append(i[2])
            return tables
        finally:
            c.close()
            conn.close()

    @classmethod
    def show_columns_win(cls, path, table):
        conn = pypyodbc.win_connect_mdb(path)
        c = conn.cursor()
        try:
            column_obj = c.columns(table).fetchall()
        except Exception as e:
            # log something
            pass
        else:
            return [column[3] for column in column_obj]
        finally:
            c.close()
            conn.close()

    def choose_converter(self):
        if self.conversion_method == 0:
            return DataGetter.hex_to_dec
        elif self.conversion_method == 1:
            return DataGetter.hex_to_dec1

    def create_query_string(self):
        query = "SELECT {} FROM {}".format(self.columns, self.table)
        return query

    @staticmethod
    def hex_to_dec(string_hex):
        decoded_1 = str(string_hex[4:6])
        decoded_2 = str(string_hex[6:10])
        new_ = str(int(decoded_1, 16)) + str(int(decoded_2, 16))
        return float(new_)

    @staticmethod
    def hex_to_dec1(string_hex):
        return float(int(string_hex, 16))

    def show_row_disposition(self):
        if not self.data:
            return
        for i in range(10):
            print(self.data[i])

    def get_data_win(self):
        conn = pypyodbc.win_connect_mdb(self.db_path)
        c = conn.cursor()
        try:
            self.data = c.execute(self.create_query_string()).fetchall()
        except Exception as e:
            # log somthing here
            raise
        else:
            self.result = [(self.converter(i[0]), i[1]) for i in self.data]
        finally:
            c.close()
            conn.close()

    def get_data_linux(self):
        try:
            self.data = list(io.read_mdb(self.db_path, table=self.table))
        except TypeError as e:
            raise

        result = []
        for obj in self.data:
            result.append((self.converter(obj[self.column1]), obj[self.column2]))

        self.result = result

    def run(self):
        if self.is_windows:
            self.get_data_win()
        else:
            self.get_data_linux()

    @classmethod
    def show_tables(cls, path):
        if cls.is_linux():
            return cls.show_tables_linux(path)
        else:
            return cls.show_tables_win(path)

    @classmethod
    def show_columns(cls, path, table):
        if cls.is_linux():
            return cls.show_columns_linux(path, table)
        else:
            return cls.show_columns_win(path, table)
