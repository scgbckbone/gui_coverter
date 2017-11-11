from mdb_fetcher import DataGetter
from xls_writer import XLSWriter

res = DataGetter(
        db_path="/home/scag/Desktop/agatova_7f_bes.mdb",
        table_name="identifikatory",
        col_names=["identifikator", "meno_majitela"],
        col_indexes=[1, 2]
).run()


wxls = XLSWriter(
    "/home/scag/Desktop/test_1.xls",
    start_date='2017-11-1',
    end_date='2099-12-31',
)

wxls.write(res)
