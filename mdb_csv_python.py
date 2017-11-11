import csv
import pyodbc

# set up some constants
MDB = '/home/scag/Desktop/agatova_7f_bes.mdb'
DRV = '{Microsoft Access Driver (*.mdb, *.accdb)}'

# connect to db
con = pyodbc.connect('DRIVER={};DBQ={}'.format(DRV, MDB))
cur = con.cursor()

# run a query and get the results
SQL = 'SELECT * FROM mytable;' # your query goes here
rows = cur.execute(SQL).fetchall()
cur.close()
con.close()

# you could change the mode from 'w' to 'a' (append) for any subsequent queries
with open('mytable.csv', 'wb') as fou:
    csv_writer = csv.writer(fou) # default field-delimiter is ","
    csv_writer.writerows(rows)