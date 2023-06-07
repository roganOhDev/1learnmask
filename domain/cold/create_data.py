import csv
import sqlite3

from const.config import db_name, cold_seongbuk_gu_code

def run(con, cur, cold_csv_path):

    to_insert_before_order = []
    values = []

    cur.execute("drop table if exists cold_grade;")
    cur.execute("drop table if exists cold;")
    cur.execute("CREATE TABLE cold(id INTEGER PRIMARY KEY AUTOINCREMENT,year TEXT, date TEXT, value INTEGER);")
    cur.execute("CREATE TABLE cold_grade \
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    grade INTEGER, \
                     value INTEGER);")
    con.commit()

    with open(cold_csv_path, 'r') as fin:
        dr = csv.DictReader(fin)

        for row in dr:
            if int(row['area_code']) == cold_seongbuk_gu_code:
                to_insert_before_order.append((row['date'][:4], row['date'][5:], int(row['value'])))
                values.append(int(row['value']))

    to_insert = sorted(to_insert_before_order, key=lambda x: (x[0], x[1]), reverse=True)
    cur.executemany("INSERT INTO cold (year, date, value) VALUES (?, ?, ?);", to_insert)
    con.commit()

    values.sort()

    i = 0
    len = values.__len__()
    chunk = int(len / 5)
    grade = 0
    for value in values:
        i += 1
        if i % chunk == 0:
            if (grade == 4):
                break

            cur.execute("INSERT INTO cold_grade (grade, value) VALUES (?,?);", (grade + 1, value))
            con.commit()

            grade += 1
