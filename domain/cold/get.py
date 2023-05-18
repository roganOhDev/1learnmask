import csv
import sqlite3

from const.config import db_name

con = sqlite3.connect("../../" + db_name)
cur = con.cursor()

with open('./data.csv', 'r') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['date'], int(i['value'])) for i in dr]

cur.executemany("INSERT INTO cold (date, value) VALUES (?, ?);", to_db)
con.commit()
con.close()
