import csv
import sqlite3

from const.config import db_name, cold_seongbuk_gu_code

con = sqlite3.connect("../../" + db_name)
cur = con.cursor()
to_insert = []

with open('./data.csv', 'r') as fin:
    dr = csv.DictReader(fin)
    to_insert = [(row['date'][:4], row['date'][5:], int(row['value'])) for row in dr if
                 int(row['area_code']) == cold_seongbuk_gu_code]

cur.executemany("INSERT INTO cold (year, date, value) VALUES (?, ?, ?);", to_insert)
con.commit()
con.close()
