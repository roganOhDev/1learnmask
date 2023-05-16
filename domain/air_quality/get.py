import datetime

import requests

from const.data_cache import get_datetime_last_air_quality_datetime
from domain.air_quality.air_quality_pm10 import AirQualityPm10
from domain.air_quality.air_quality_pm25 import AirQualityPm25
from domain.update_cache import set_datetime_last_air_quality_datetime
from utils import log
from utils.log import logger
from utils.time_utils import string_to_datetime_air_quality


def get():
    if __check_not_have_to_get_data():
        logger.info("not have to update data")
        return

    jj = __connect_api()

    totalCount = jj.get("response").get("body").get("totalCount")
    base = jj.get("response").get("body").get("items")

    __create(base, totalCount)


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


def __create(base, total_count: int):
    first_data_time = base[0].get('dataTime')

    for i in range(total_count):
        now_data = base[i]
        now_data_time = string_to_datetime_air_quality(now_data.get('dataTime'))

        __create_pm_10_data(now_data, now_data_time)
        __create_pm_25_data(now_data, now_data_time)

    set_datetime_last_air_quality_datetime(first_data_time)


def __create_pm_10_data(now_data, now_data_time: datetime.datetime):
    if now_data_time > get_datetime_last_air_quality_datetime():
        log.logger.info("new data : " + now_data.get('dataTime') + " , (pm10Value)")
        AirQualityPm10(now_data.get('dataTime'), now_data.get('pm10Value')).save()

    else:
        log.logger.info("existing data : " + now_data.get('dataTime') + " , (pm10Value)")


def __create_pm_25_data(now_data, now_data_time: datetime.datetime):
    if now_data_time > get_datetime_last_air_quality_datetime():
        log.logger.info("new data : " + now_data.get('dataTime') + " , (pm25Value)")
        AirQualityPm25(now_data.get('dataTime'), now_data.get('pm25Value')).save()

    else:
        log.logger.info("existing data : " + now_data.get('dataTime') + " , (pm25Value)")


def __check_not_have_to_get_data() -> bool:
    if get_datetime_last_air_quality_datetime() >= datetime.datetime.now() - datetime.timedelta(hours=1):
        return True
    else:
        return False
