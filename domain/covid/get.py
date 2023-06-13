import datetime

from const.config import covid_url
from const.data_cache import get_last_covid_update_date, get_last_covid_date
from domain.covid.covid import Covid
from domain.update_cache import __set_date_last_covid_created_date
from grade_type import GradeType
from utils import log
from utils.log import logger

import requests
from bs4 import BeautifulSoup

from utils.time_utils import string_to_date_include_year


def get_30_days_data():
    today = datetime.date.today()
    before_30_days = today - datetime.timedelta(days=30)

    data = [(element._data[0].date, element._data[0].value) for element in Covid.get_30_days_data()]
    return data


def get_new():
    response = requests.get(covid_url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    value_table = soup.find("div", class_="data_table mgt16 tbl_scrl_m mini").find("table", class_="num")
    dates = [str(datetime.datetime.now().year) + "-" + str(value.text[:-1].replace(".", "-")) for value in
             value_table.find("thead").find_all("th")[1:]][:-1]
    values = [value.text.replace(",", "") for value in value_table.find("tbody").find_all("td")][:-1]

    zipped = list(zip(dates, values))
    return zipped

def just_get() -> GradeType:
    if cnt_week_doubling():
        return GradeType.VERY_BAD
    else:
        return GradeType.VERY_GOOD

def get() -> GradeType:
    if __check_not_have_to_get_data():
        logger.info("not have to update data : covid")

    else:
        covid_values = get_new()

        for element in covid_values:
            __check_and_save_in_db(element)

        __set_date_last_covid_created_date(datetime.date.today())

    if cnt_week_doubling():
        return GradeType.VERY_BAD
    else:
        return GradeType.VERY_GOOD


def cnt_week_doubling() -> bool:
    doubling_cnt = 0
    week_data = Covid.get_week_data()
    comparison_data = Covid.get_two_weeks_ago_data()

    for data_set in zip(week_data, comparison_data):
        this_value = data_set[0]._data[0].value
        comparison_value = data_set[1]._data[0].value

        if this_value >= 2 * comparison_value:
            doubling_cnt += 1

    if doubling_cnt >= 3:
        return True
    else:
        return False


def is_week_doubling() -> bool:
    week_data = Covid.get_week_data()
    comparison_data = Covid.get_two_weeks_ago_data()

    for data_set in zip(week_data, comparison_data):
        this_value = data_set[0]._data[0].value
        comparison_value = data_set[1]._data[0].value

        return this_value >= 2 * comparison_value


def __check_and_save_in_db(element):
    date = element[0]
    value = element[1]

    __create_covid_data(Covid(value, date))


def __create_covid_data(covid: Covid):
    if string_to_date_include_year(covid.date) > get_last_covid_update_date() or string_to_date_include_year(covid.date) > get_last_covid_date():
        log.logger.info("covid new data : " + str(covid.date) + " , " + str(covid.value))
        covid.save()


def __check_not_have_to_get_data() -> bool:
    if get_last_covid_update_date() >= datetime.date.today():
        return True
    else:
        return False
