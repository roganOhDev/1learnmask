import csv
import datetime
import sqlite3

from const.config import db_name, cold_seongbuk_gu_code

def run(con, cur, covid_csv_path):
    to_insert_before_sort = []

    cur.execute("drop table if exists cold_grade;")
    cur.execute("drop table if exists cold;")
    cur.execute("CREATE TABLE cold(id INTEGER PRIMARY KEY AUTOINCREMENT,year TEXT, date TEXT, value INTEGER);")
    cur.execute("CREATE TABLE cold_grade \
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    grade INTEGER, \
                     value INTEGER);")
    con.commit()

    with open(covid_csv_path, 'r') as fin:
        dr = csv.DictReader(fin)

        for row in dr:
            to_insert_before_sort.append((row['date'], int(row['value']), str((datetime.datetime.now() - datetime.timedelta(days=1)).date())))

        to_insert_after_sort = sorted(to_insert_before_sort, key=lambda x: x[0], reverse=True)

    cur.executemany("INSERT INTO covid (date, value, created_at) VALUES (?, ?, ?);", to_insert_after_sort)
    con.commit()


