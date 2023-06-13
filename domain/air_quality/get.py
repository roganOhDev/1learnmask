import datetime

import requests

from const.data_cache import get_datetime_last_air_quality_datetime
from domain.air_quality.air_quality import AirQuality
from domain.air_quality.fine_air_quality_grade_type import FineAirQualityGradeType
from domain.update_cache import set_datetime_last_air_quality_datetime
from utils import log
from utils.log import logger
from utils.time_utils import string_to_datetime_air_quality


def get_2_days_data():
    today = datetime.datetime.today()
    before_2_days = today - datetime.timedelta(days=2)

    data = [(element._data[0].dataTime, element._data[0].pm10Value, element._data[0].pm25Value) for element in
            AirQuality.get_2_days_data(str(before_2_days))]

    return data

def just_get() -> (int, int):
    latest_data = AirQuality.get_latest_data()._data[0]
    pm10 = latest_data.get_pm_10_value()
    pm25 = latest_data.get_pm_25_value()
    pm10_grade = FineAirQualityGradeType.check_grade(pm10)
    pm25_grade = FineAirQualityGradeType.check_grade(pm25)

    return pm10_grade.value, pm25_grade.value

def get() -> (int, int):
    if __check_not_have_to_get_data():
        logger.info("not have to update data : air_quality")

    else:
        jj = __connect_api()

        base = jj.get("response").get("body").get("items")

        __create(base)

    latest_data = AirQuality.get_latest_data()._data[0]
    pm10 = latest_data.get_pm_10_value()
    pm25 = latest_data.get_pm_25_value()
    pm10_grade = FineAirQualityGradeType.check_grade(pm10)
    pm25_grade = FineAirQualityGradeType.check_grade(pm25)

    return pm10_grade.value, pm25_grade.value


def __connect_api():
    API_KEY = "hMCnLw61n9VHoITCdhn5UnQZvRZElx7ouyaGDdwzOKwA6oAWxPy7KHR2KdBsaHd82kKar3S32+WwSk/F5ibmmg=="
    params = {
        'serviceKey': API_KEY,
        'returnType': 'json',
        'numOfRows': '5000',
        'pageNo': '1',
        'stationName': '성북구',
        'dataTerm': '3MONTH',
        'ver': '1.0'
    }
    url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty'
    res = requests.get(url, params)

    return res.json()


def __create(base):
    first_data_time = base[0].get('dataTime')

    for now_data in base:
        now_data_time = string_to_datetime_air_quality(now_data.get('dataTime'))

        __create_data(now_data, now_data_time)

    set_datetime_last_air_quality_datetime(first_data_time)


def __create_data(now_data, now_data_time: datetime.datetime):
    if now_data_time > get_datetime_last_air_quality_datetime():
        log.logger.info("air quality new data : " + now_data.get('dataTime') + " , (air_quality)")
        AirQuality(now_data.get('dataTime'), now_data.get('pm10Value'), now_data.get('pm25Value')).save()


def __check_not_have_to_get_data() -> bool:
    if get_datetime_last_air_quality_datetime() >= datetime.datetime.now() - datetime.timedelta(hours=1) - datetime.timedelta(minutes=30):
        return True
    else:
        return False
