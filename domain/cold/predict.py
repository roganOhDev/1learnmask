import sqlite3
import datetime

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf

from domain.cold.cold import Cold

tf.random.set_seed(777) #하이퍼파라미터 튜닝을 위해 실행시 마다 변수가 같은 초기값 가지게 하기
import numpy as np
#matplotlib 패키지 한글 깨짐 처리 시작
import matplotlib.pyplot as plt
import platform
if platform.system() == 'Darwin': #맥
        plt.rc('font', family='AppleGothic')
elif platform.system() == 'Windows': #윈도우
        plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Linux': #리눅스 (구글 콜랩)
        #!wget "https://www.wfonts.com/download/data/2016/06/13/malgun-gothic/malgun.ttf"
        #!mv malgun.ttf /usr/share/fonts/truetype/
        #import matplotlib.font_manager as fm
        #fm._rebuild()
        plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False #한글 폰트 사용시 마이너스 폰트 깨짐 해결
#matplotlib 패키지 한글 깨짐 처리 끝
# %matplotlib inline

def load_time_series_data(data, sequence_length):
    #print(data.shape) #(1225, 1)
    #print(sequence_length) #3
    window_length = sequence_length + 1
    x_data = []
    y_data = []
    for i in range(0, len(data) - window_length + 1): #0 1 2 3 4 5 6 7 8 9 | 10
        window = data[i:i + window_length, :]
        x_data.append(window[:-1, :])
        y_data.append(window[-1, [-1]])
    x_data = np.array(x_data)
    y_data = np.array(y_data)
    #print(x_data.shape) #(1222, 3, 1)
    #print(y_data.shape) #(1222, 1)

    return x_data, y_data

##########데이터 로드
conn = sqlite3.connect('../../data.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Execute the SQL query to select all data from a table
cursor.execute('SELECT * FROM cold')

# Fetch all the rows returned by the query
rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
df = pd.DataFrame(rows, columns=columns)

##########데이터 분석

print(df.head())

print(df.info())

print(df.describe())

##########데이터 전처리

today = str(datetime.datetime.now())[5:10]
# df = df[df['date'] == today]
df = df.sort_values(by='year')

data = df[['value']].to_numpy()
print(data.shape) #((720, 1)

transformer = MinMaxScaler()
data = transformer.fit_transform(data)

sequence_length = 3
x_data, y_data = load_time_series_data(data, sequence_length)
print(x_data.shape) #((717, 3, 1)
print(y_data.shape) #(717, 1)

x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.3, shuffle=False) #시각화를 위해 shuffle=False 옵션 사용
print(x_train.shape) #((501, 3, 1)
print(y_train.shape) #(501, 1)
print(x_test.shape) #(216, 3, 1)
print(y_test.shape) #(216, 1)

##########모델 생성

input = tf.keras.layers.Input(shape=(sequence_length, 1))
net = tf.keras.layers.LSTM(units=32, activation='relu')(input)
net = tf.keras.layers.Dense(units=32, activation='relu')(net)
net = tf.keras.layers.Dense(units=1)(net)
model = tf.keras.models.Model(input, net)

##########모델 학습

model.compile(loss='mean_squared_error', optimizer='adam')

model.fit(x_train, y_train, epochs=50, validation_data=(x_test, y_test))

##########모델 검증

##########모델 예측

def plot(data, y_predict_train, y_predict_test):
    plt.plot(transformer.inverse_transform(data)[:, [-1]].flatten(), label='실제 감기 확진자 수')

    y_predict_train = transformer.inverse_transform(y_predict_train)
    y_predict_train_plot = np.empty_like(data[:, [0]])
    y_predict_train_plot[:, :] = np.nan
    y_predict_train_plot[sequence_length:len(y_predict_train) + sequence_length, :] = y_predict_train
    plt.plot(y_predict_train_plot.flatten(), label='학습 데이터 예측 종가')

    y_predict_test = transformer.inverse_transform(y_predict_test)
    y_predict_test_plot = np.empty_like(data[:, [0]])
    y_predict_test_plot[:, :] = np.nan
    y_predict_test_plot[len(y_predict_train) + sequence_length:, :] = y_predict_test
    plt.plot(y_predict_test_plot.flatten(), label='테스트 데이터 예측 종가')

    plt.legend()
    plt.show()

y_predict_train = model.predict(x_train)
y_predict_test = model.predict(x_test)
# plot(data, y_predict_train, y_predict_test)

x_test = np.array([
        [[44], [49], [50]]
])
x_test = x_test.reshape(-1, 1)
x_test = transformer.transform(x_test)
x_test = x_test.reshape(1, sequence_length, 1)

y_predict = model.predict(x_test)

y_predict = transformer.inverse_transform(y_predict)
print(y_predict[0][0])