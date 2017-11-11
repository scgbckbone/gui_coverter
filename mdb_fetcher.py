import sys
import pypyodbc
from meza import io


class InvalidInputError(Exception):
    """When both indexes and columns are not specified."""


class DataGetter(object):
    def __init__(self, db_path, table_name, col_names=None, col_indexes=None,
                 conversion_method=0):
        self.db_path = db_path
        self.table = table_name
        self.columns = col_names
        self.indexes = col_indexes
        self.validate = self.validate_input()
        self.conversion_method = conversion_method
        self.converter = self.choose_converter()
        self.data = None
        self.result = None

    @property
    def is_windows(self):
        if sys.platform == "win32" or sys.platform == "win64":
            return True
        return False

    def choose_converter(self):
        if self.conversion_method == 0:
            return DataGetter.hex_to_dec
        elif self.conversion_method == 1:
            return DataGetter.hex_to_dec1

    def validate_input(self):
        if not self.columns and not self.indexes:
            raise InvalidInputError("Unsufficient arguments.")

    def create_query_string(self):
        if not self.columns:
            columns = "*"
        else:
            columns = ",".join(self.columns) if len(self.columns) > 1 else self.columns[0]
        query = "SELECT {} FROM {}".format(columns, self.table)
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

    def run(self):
        if self.is_windows:
            conn = pypyodbc.win_connect_mdb(self.db_path)
            c = conn.cursor()
            try:
                self.data = c.execute(self.create_query_string()).fetchall()
                result = []
                for d in self.data:
                    result.append((d[0], d[1]))
            except Exception as e:
                # log somthing here
                raise
            else:
                self.result = result

            finally:
                c.close()
                conn.close()

        else:
            try:
                self.data = list(io.read_mdb(self.db_path, table=self.table))
            except TypeError as e:
                print(80*"=")
                raise

            result = []
            for i in self.data:
                if not self.columns:
                    raise InvalidInputError("Provide desired column names.")
                intermediate_res = []
                for column in self.columns:
                    try:
                        if column == "identifikator":
                            x = self.hex_to_dec(i[column])
                        else:
                            x = i[column]
                        intermediate_res.append(x)
                    except KeyError:
                        raise InvalidInputError("Columns don't match.")
                result.append(intermediate_res)

            self.result = result


if __name__ == "__main__":

    o = DataGetter(
        db_path="/home/scag/Desktop/agatova_7f_bes.mdb",
        table_name="identifikatory",
        col_names=["identifikator", "meno_majitela"],
        col_indexes=[1, 2]
    )
    res = o.run()
    x = 0
    print("here i started to print")