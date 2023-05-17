import csv, sqlite3

from const.config import db_name

con = sqlite3.connect("./" + db_name)  # change to 'sqlite:///your_filename.db'
cur = con.cursor()
cur.execute("CREATE TABLE cold(id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, value INTEGER);")  # use your column names here

with open('./cold/data.csv', 'r') as fin:  # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin)  # comma is default delimiter
    to_db = [(i['col1'], i['col2']) for i in dr]

cur.executemany("INSERT INTO cold (date, col2) VALUES (?, ?);", to_db)
con.commit()
con.close()
