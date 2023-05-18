import datetime
from domain.cold.cold import Cold


def get() -> int:
    now = datetime.datetime.now()
    cold_data = Cold.get_all_by_date(now)

    sum = 0
    for e in cold_data:
        sum += e._data[0].value

    response = sum / cold_data.__len__()

    return int(response)
