import datetime

from const import data_cache
from const.data_cache import get_last_covid_update_date
from domain.air_quality.air_quality import AirQuality
from domain.covid.covid import Covid
from utils.log import logger
from domain.cold import get as get_cold
from utils.time_utils import string_to_date_include_year


def run():
    __init_covid_cache()
    __init_air_quality_cache()
    __init_cold_cache()
    logger.info("last_covid_updated_at : " + str(get_last_covid_update_date()))
    logger.info("air_quality_cache : " + str(data_cache.last_air_quality_datetime))
    logger.info("cold_cache : " + str(data_cache.last_cold_value))


def __init_covid_cache():
    covid = Covid.get_latest_data()
    if covid:
        data_cache.last_covid_update_date = string_to_date_include_year(covid._data[0].created_at)
        data_cache.last_cold_date = string_to_date_include_year(covid._data[0].date)


def __set_date_last_covid_created_date(date: datetime.date):
    data_cache.last_covid_update_date = date


def __init_air_quality_cache():
    air_quality = AirQuality.get_latest_data()
    if air_quality:
        data_cache.last_air_quality_datetime = air_quality._data[0].dataTime


def __init_cold_cache():
    data_cache.last_cold_value = get_cold.learn()
    data_cache.last_cold_date = datetime.date.today()


def set_datetime_last_air_quality_datetime(datetime: str):
    data_cache.last_air_quality_datetime = datetime


def set_yellow_dust_cache(datetime_: datetime.datetime, value: int):
    data_cache.last_yellow_dust.datetime = datetime_
    data_cache.last_yellow_dust.value = value
