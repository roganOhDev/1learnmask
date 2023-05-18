import datetime

from const import data_cache
from domain.air_quality.air_quality_pm10 import AirQualityPm10
from domain.covid.covid import Covid
from domain.yellow_dust.yellow_dust import YellowDust
from utils.log import logger


def run():
    __init_covid_cache()
    __init_air_quality_cache()
    logger.info("covid_date_cache : " + data_cache.last_covid_date)
    logger.info("air_quality_cache : " + data_cache.last_air_quality_datetime)


def __init_covid_cache():
    covid = Covid.get_latest_data()
    if covid:
        data_cache.last_covid_date = covid._data[0].date


def __set_date_last_covid_date(date):
    data_cache.last_covid_date = date


def __init_air_quality_cache():
    air_quality = AirQualityPm10.get_latest_data()
    if air_quality:
        data_cache.last_air_quality_datetime = air_quality._data[0].dataTime


def set_datetime_last_air_quality_datetime(datetime: str):
    data_cache.last_air_quality_datetime = datetime


def set_yellow_dust_cache(datetime_: datetime.datetime, value: int):
    data_cache.last_yellow_dust.datetime = datetime_
    data_cache.last_yellow_dust.value = value
