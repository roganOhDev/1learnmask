import sqlite3

from const.config import db_name
from domain.cold import create_data
from domain.covid import backup_covid_data

con = sqlite3.connect("./" + db_name)
cur = con.cursor()

covid_csv_path = 'domain/covid/covid.csv'
cold_csv_path = 'domain/cold/data.csv'

backup_covid_data.run(con, cur, covid_csv_path)
create_data.run(con, cur, cold_csv_path)

con.close()