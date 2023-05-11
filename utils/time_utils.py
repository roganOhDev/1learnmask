import datetime
from datetime import datetime as dt

import time


def get_unix_time(real_datetime: datetime) -> float:
    return time.mktime(real_datetime.timetuple())


def get_date_time(unix_time: float) -> datetime:
    return dt.utcfromtimestamp(unix_time)
