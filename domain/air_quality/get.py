import logging

import requests

from domain.air_quality.air_quality_pm10 import AirQualityPm10
from domain.air_quality.air_quality_pm25 import AirQualityPm25
from utils import log


def get():
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
    for i in range(total_count):
        now_data = base[i]

        __create_pm_10_data(now_data)
        __create_pm_25_data(now_data)


def __create_pm_10_data(now_data):
    existing_data = AirQualityPm10.select(now_data.get('dataTime'))
    if not existing_data:
        log.logger.info("new data : " + now_data.get('dataTime') + " , (pm10Value)")
        AirQualityPm10(now_data.get('dataTime'), now_data.get('pm10Value')).save()
    else:
        log.logger.info("existing data : " + now_data.get('dataTime') + " , (pm10Value)")


def __create_pm_25_data(now_data):
    existing_data = AirQualityPm25.select(now_data.get('dataTime'))
    if not existing_data:
        log.logger.info("new data : " + now_data.get('dataTime') + " , (pm25Value)")
        AirQualityPm25(now_data.get('dataTime'), now_data.get('pm25Value')).save()
    else:
        log.logger.info("existing data : " + now_data.get('dataTime') + " , (pm25Value)")
