import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from const.config import driver_path, covid_url
from const.data_cache import get_date_last_covid
from domain.covid.covid import Covid
from domain.update_cache import __set_date_last_covid_date
from utils import log


def get():
    driver = __get_chrome_driver()
    covid_values = __get_covid_data_with_crowl(driver)

    first_day = __get_first_day_of_crowl(covid_values)
    element_date = first_day

    for element in covid_values:
        __check_and_save_in_db(element, element_date)
        element_date += datetime.timedelta(days=1)

    __set_date_last_covid_date(element_date)

    driver.quit()


def __get_chrome_driver() -> WebDriver:
    service = Service(driver_path)
    options = Options()
    options.add_argument('--headless')
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
        log.logger.info("new data : " + str(covid.date) + " , " + str(covid.value))
        covid.save()
    else:
        log.logger.info("existing data : " + str(covid.date) + " , " + str(covid.value))
