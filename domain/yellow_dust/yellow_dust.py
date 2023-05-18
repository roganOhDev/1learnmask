from datetime import datetime as dt


class YellowDust:
    datetime: dt
    value: int

    def __init__(self):
        self.datetime = dt.min
        self.value = 0

    def set_date(self, datetime: dt):
        self.datetime = datetime

    def set_value(self, value: int):
        self.value = value
