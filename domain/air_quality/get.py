import requests
import sqlite3
date = []
pm10 = []

conn = sqlite3.connect('data.db')
cursor = conn.cursor()
API_KEY = "hMCnLw61n9VHoITCdhn5UnQZvRZElx7ouyaGDdwzOKwA6oAWxPy7KHR2KdBsaHd82kKar3S32+WwSk/F5ibmmg=="
params = {
    'serviceKey' : API_KEY,
    'returnType' : 'json',
    'numOfRows' : '5000',
    'pageNo' : '1',
    'stationName': '성북구',
    'dataTerm': '3MONTH',
    'ver': '1.0'
}
url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty'
res = requests.get(url, params)

jj = res.json()
totalCount = jj.get("response").get("body").get("totalCount")
base = jj.get("response").get("body").get("items")

cursor.execute('''CREATE TABLE IF NOT EXISTS air_quality10
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 dataTime TEXT,
                 pm10Value INTEGER)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS air_quality25
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 dataTime TEXT,
                 pm25Value INTEGER)''')

for i in range(totalCount):
    dataTime = base[i].get('dataTime')
    cursor.execute("SELECT * FROM air_quality10 WHERE dataTime=?", (dataTime,))
    existing_data = cursor.fetchone()
    if not existing_data:
        cursor.execute('INSERT INTO air_quality10 (dataTime, pm10Value) VALUES (?, ?)',
                      (base[i].get('dataTime'), base[i].get('pm10Value')))
    cursor.execute("SELECT * FROM air_quality25 WHERE dataTime=?", (dataTime,))
    existing_data = cursor.fetchone()
    if not existing_data:
        cursor.execute('INSERT INTO air_quality25 (dataTime, pm25Value) VALUES (?, ?)',
                      (base[i].get('dataTime'), base[i].get('pm25Value')))
    
    
conn.commit()
conn.close()

