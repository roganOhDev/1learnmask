import datetime

from const.data_cache import get_date_last_covid
from domain.covid.covid import Covid
from domain.update_cache import __set_date_last_covid_date
from grade_type import GradeType
from utils import log
from utils.log import logger

import requests
from bs4 import BeautifulSoup

from utils.time_utils import string_to_date_covid


def get_30_days_data():
    today = datetime.date.today()
    before_30_days = today - datetime.timedelta(days=30)

    data = [(element._data[0].date, element._data[0].value) for element in Covid.get_30_days_data(str(before_30_days))]
    return data


def get_new():
    if __check_not_have_to_get_data():
        logger.info("not have to update data : covid")

    else:
        url = "https://ncov.kdca.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun="
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        value_table = soup.find("div", class_="data_table mgt16 tbl_scrl_m mini").find("table", class_="num")
        dates = [str(datetime.datetime.now().year) + "-" + str(value.text[:-1].replace(".", "-")) for value in
                         value_table.find("thead").find_all("th")[1:]][:-1]
        values = [value.text.replace(",", "") for value in value_table.find("tbody").find_all("td")][:-1]

        zipped = list(zip(dates, values))
        return zipped


def get() -> GradeType:
    if __check_not_have_to_get_data():
        logger.info("not have to update data : covid")

    else:
        covid_values = get_new()

        for element in covid_values:
            __check_and_save_in_db(element)

        __set_date_last_covid_date(covid_values[-1][0])

    if cnt_week_doubling():
        return GradeType.VERY_BAD
    else:
        return GradeType.VERY_GOOD


def cnt_week_doubling() -> bool:
    today = datetime.date.today()
    check = 7
    doubling_cnt = 0
    while check != 0:
        date = today - datetime.timedelta(days=check)
        if is_week_doubling(date):
            doubling_cnt += 1

        check -= 1

    if doubling_cnt >= 3:
        return True
    else:
        return False


def is_week_doubling(date: datetime.date) -> bool:
    last_week = date - datetime.timedelta(weeks=1)
    last_week_string = str(last_week)
    today_string = str(date)
    last_week_value = Covid.get_by_date(last_week_string)._data[0].value
    today_value_json = Covid.get_by_date(today_string)

    if today_value_json == None:
        date_string = str(date - datetime.timedelta(days=7))
        last_week_string = str(date - datetime.timedelta(days=14))
        last_week_value = Covid.get_by_date(last_week_string)._data[0].value
        today_value_json = Covid.get_by_date(date_string)

    today_value = today_value_json._data[0].value
    return today_value >= 2 * last_week_value


def __check_and_save_in_db(element):
    date = element[0]
    value = element[1]

    __create_covid_data(Covid(value, date))


def __create_covid_data(covid: Covid):
    if get_date_last_covid() == "" or string_to_date_covid(covid.date) > get_date_last_covid():
        log.logger.info("covid new data : " + str(covid.date) + " , " + str(covid.value))
        covid.save()


def __check_not_have_to_get_data() -> bool:
    if get_date_last_covid() >= datetime.date.today() - datetime.timedelta(days=1):
        return True
    else:
        return False
