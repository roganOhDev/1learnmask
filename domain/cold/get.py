import datetime
import sqlite3

import matplotlib.pyplot as plt
import platform
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf

from const.config import db_name
from const import data_cache
from grade_type import GradeType
from utils.log import logger


def learn() -> int:
    if data_cache.last_cold_date == datetime.date.today():
        logger.info("not have to update data : cold")
        return data_cache.last_cold_value

    tf.random.set_seed(777)  # 하이퍼파라미터 튜닝을 위해 실행시 마다 변수가 같은 초기값 가지게 하기
    # matplotlib 패키지 한글 깨짐 처리 시작
    if platform.system() == 'Darwin':  # 맥
        plt.rc('font', family='AppleGothic')
    elif platform.system() == 'Windows':  # 윈도우
        plt.rc('font', family='Malgun Gothic')
    elif platform.system() == 'Linux':  # 리눅스 (구글 콜랩)
        plt.rc('font', family='Malgun Gothic')
    plt.rcParams['axes.unicode_minus'] = False  # 한글 폰트 사용시 마이너스 폰트 깨짐 해결

    def load_time_series_data(data, sequence_length):
        window_length = sequence_length + 1
        x_data = []
        y_data = []
        for i in range(0, len(data) - window_length + 1):  # 0 1 2 3 4 5 6 7 8 9 | 10
            window = data[i:i + window_length, :]
            x_data.append(window[:-1, :])
            y_data.append(window[-1, [-1]])
        x_data = np.array(x_data)
        y_data = np.array(y_data)

        return x_data, y_data

    ##########데이터 로드
    conn = sqlite3.connect(db_name)

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Execute the SQL query to select all data from a table
    cursor.execute("SELECT * FROM cold")

    # Fetch all the rows returned by the query
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(rows, columns=columns)

    ##########데이터 분석

    ##########데이터 전처리

    df = df.sort_values(by='year')

    data = df[['value']].to_numpy()

    transformer = MinMaxScaler()
    data = transformer.fit_transform(data)

    sequence_length = 3
    x_data, y_data = load_time_series_data(data, sequence_length)

    x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.3,
                                                        shuffle=False)  # 시각화를 위해 shuffle=False 옵션 사용

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

    x_test = np.array([
        [[44], [49], [50]]
    ])
    x_test = x_test.reshape(-1, 1)
    x_test = transformer.transform(x_test)
    x_test = x_test.reshape(1, sequence_length, 1)

    y_predict = model.predict(x_test)

    y_predict = transformer.inverse_transform(y_predict)

    data_cache.last_cold_date = datetime.date.today()
    data_cache.last_cold_value = int(y_predict[0][0])

    return int(y_predict[0][0])


def get() -> GradeType:
    learn()
    return __check_grade(data_cache.last_cold_value)


def __check_grade(value: int) -> GradeType:
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    grades = cur.execute("SELECT * FROM cold_grade order by grade").fetchall()
    grade_arr = [grade[2] for grade in grades]

    if value <= grade_arr[0]:
        return GradeType.VERY_GOOD
    elif grade_arr[0] < value & value <= grade_arr[1]:
        return GradeType.GOOD
    elif grade_arr[1] < value & value <= grade_arr[2]:
        return GradeType.MEDIUM
    elif grade_arr[2] < value & value <= grade_arr[3]:
        return GradeType.BAD
    elif grade_arr[3] < value:
        return GradeType.VERY_BAD
