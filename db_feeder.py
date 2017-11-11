from xlrd import open_workbook
from xlutils.copy import copy
from converters import create_map


rb = open_workbook("/home/scag/Desktop/eee.xls", formatting_info=True)
sheet = rb.sheets()[0]
wb = copy(rb)
s = wb.get_sheet(0)

mappa = create_map("/home/scag/Desktop/agatova.csv", 0, 1, "identifikator")

counter = 0
for lst in sheet._cell_values:
    print("before", lst)
    if counter == 0:
        for i in range(len(lst)):
            s.write(counter, i, lst[i])
        counter += 1
        continue
    lst[0] = (10 - len(str(counter))) * " " + str(counter)
    lst[1] = mappa[counter][0]
    lst[2] = mappa[counter][1]
    lst[5] = start_date if start_date else lst[5]
    print("after", lst)
    print(counter)
    print(len(lst[0]))
    for i in range(len(lst)):
        s.write(counter, i, lst[i])
    counter += 1

#  s.write(row, column, data)
wb.save('/home/scag/Desktop/names.xls')
