import datetime

from domain.yellow_dust.yellow_dust import YellowDust
from utils.time_utils import string_to_datetime_air_quality, string_to_date_covid

last_covid_date = ""
last_air_quality_datetime = ""
last_yellow_dust = YellowDust()


def get_datetime_last_air_quality_datetime():
    if last_air_quality_datetime == "":
        return datetime.datetime.min
    else:
        return string_to_datetime_air_quality(last_air_quality_datetime)


def get_date_last_covid() -> datetime.date:
    if last_covid_date == "":
        return datetime.datetime.min.date()
    else:
        return string_to_date_covid(last_covid_date)


def get_date_last_yellow_dust() -> datetime.datetime:
    return last_yellow_dust.datetime
