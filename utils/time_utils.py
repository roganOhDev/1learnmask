import datetime
from datetime import datetime as dt

import time


def get_unix_time(real_datetime: datetime) -> float:
    return time.mktime(real_datetime.timetuple())


def get_date_time(unix_time: float) -> datetime:
    return dt.utcfromtimestamp(unix_time)


def string_to_datetime_air_quality(string: str):
    if string.endswith(' 24:00'):
        original_time = string.replace(' 24:00', ' 00:00')
        parsed_time = dt.strptime(original_time, '%Y-%m-%d %H:%M')
        return parsed_time + datetime.timedelta(days=1)

    else:
        return dt.strptime(string, '%Y-%m-%d %H:%M')


def string_to_date_covid(string: str) -> datetime.date:
    return dt.strptime(string, '%Y-%m-%d').date()


def datetime_to_string_air_quality(datetime):
    return datetime.strftime('%Y-%m-%d %H:%M')


def date_to_string_covid(date):
    return date.strftime('%m.%d')
