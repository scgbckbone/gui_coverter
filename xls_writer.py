from xlwt import Workbook


class XLSWriter(object):
    columns = ['User ID', 'User Name', 'Card NO', 'Dochádzka',
               'Kontrola prístupu',
               'Začiatok platnosti', 'Koniec platnosti', 'Department']
    start = 1

    def __init__(self, out_file, start_date="2017-11-1", end_date="2099-12-1",
                 sheet_name="ExcelData"):
        self.out_file = out_file
        self.start_date = start_date
        self.end_date = end_date
        self.sheet_name = sheet_name
        self.wb = None
        self.sheet = None

    def pre_process(self):
        self.wb = Workbook()
        self.sheet = self.wb.add_sheet(self.sheet_name)

        for i in range(len(self.columns)):
            self.sheet.write(0, i, self.columns[i])

    def write_windows(self, data_):
        pass

    def write_linux(self, data_):
        pass

    def save_file(self):
        self.wb.save(self.out_file)

    def write(self, data_):
        self.pre_process()
        for counter, data in enumerate(data_, start=self.start):
            self.sheet.write(
                counter, 0, (10 - len(str(counter))) * " " + str(counter)
            )
            self.sheet.write(counter, 1, data[1])
            self.sheet.write(counter, 2, float(data[0]))
            self.sheet.write(counter, 3, float(1))
            self.sheet.write(counter, 4, float(1))
            self.sheet.write(counter, 5, self.start_date)
            self.sheet.write(counter, 6, self.end_date)
            self.sheet.write(counter, 7, "")
        self.save_file()


