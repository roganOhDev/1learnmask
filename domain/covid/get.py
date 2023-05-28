import datetime

from selenium.webdriver.chrome import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from const.config import covid_url, service, options
from const.data_cache import get_date_last_covid
from domain.covid.covid import Covid
from domain.update_cache import __set_date_last_covid_date
from grade_type import GradeType
from utils import log
from utils.log import logger
from selenium import webdriver


def get_30_days_data():
    today = datetime.date.today()
    before_30_days = today - datetime.timedelta(days=30)

    data = [(element._data[0].date, element._data[0].value) for element in Covid.get_30_days_data(str(before_30_days))]
    return data


def get() -> GradeType:
    if __check_not_have_to_get_data():
        logger.info("not have to update data : covid")

    else:
        driver = __get_chrome_driver()
        covid_values = __get_covid_data_with_crowl(driver)

        first_day = __get_first_day_of_crowl(covid_values)
        element_date = first_day

        for element in covid_values:
            __check_and_save_in_db(element, element_date)
            element_date += datetime.timedelta(days=1)

        __set_date_last_covid_date(element_date)

        driver.quit()

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


def __get_chrome_driver() -> WebDriver:
    chrome_driver = webdriver.Chrome(service=service, options=options)
    chrome_driver.get(covid_url)

    return chrome_driver


def __create_dynamic_data_waiter(driver: WebDriver) -> WebDriverWait:
    element = driver.find_element(By.CSS_SELECTOR,
                                  "div._infect_content[data-type='status'][data-param='u1=1'][style='display: block;']")

    return WebDriverWait(element, 10)


def __get_covid_data_with_crowl(driver: WebDriver):
    wait = __create_dynamic_data_waiter(driver)

    graph = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'dl.data_content.-bar_thin.-bar_data._x_axis_and_series_label'))
    )

    return graph.find_elements(By.CSS_SELECTOR, "div.column._column")


def __get_first_day_of_crowl(covid_values) -> datetime.date:
    date_string = covid_values[0].find_element(By.CSS_SELECTOR, "dt.x_axis_value").text
    return datetime.date(datetime.datetime.now().year, int(date_string.split('.')[0]),
                         int(date_string.split('.')[1]))


def __check_and_save_in_db(element, date):
    span = element.find_element(By.CSS_SELECTOR, "span.text")
    value = span.get_attribute('innerText').replace(',', '').replace('최저', '').replace('최고', '').strip()

    __create_covid_data(Covid(value, date))


def __create_covid_data(covid: Covid):
    if covid.date > get_date_last_covid():
        log.logger.info("covid new data : " + str(covid.date) + " , " + str(covid.value))
        covid.save()


def __check_not_have_to_get_data() -> bool:
    if get_date_last_covid() >= datetime.date.today() - datetime.timedelta(days=1):
        return True
    else:
        return False
