import datetime

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from const.config import yellow_dust_url, chrome_driver
from const.data_cache import get_date_last_yellow_dust
from domain.update_cache import set_yellow_dust_cache
from utils.log import logger


def get() -> int:
    if __check_not_have_to_get_data():
        logger.info("not have to update data : yellow_dust")
        return

    driver = __get_chrome_driver()
    now_datetime, value = __get_yellow_dust_data_with_crowl(driver)

    set_yellow_dust_cache(now_datetime, value)

    driver.quit()

    return int(value)


def __get_chrome_driver() -> WebDriver:
    chrome_driver.get(yellow_dust_url)

    return chrome_driver


def __create_dynamic_data_waiter(driver: WebDriver) -> WebDriverWait:
    element = driver.find_elementelement = driver.find_element(By.CSS_SELECTOR,
                                                               'span.ct09.lv1._local[data-local-name="서울"][data-fill-color="#cce7ff"][href*="%EC%84%9C%EC%9A%B8%20%ED%99%A9%EC%82%AC"]')

    return WebDriverWait(element, 10)


def __get_yellow_dust_data_with_crowl(driver: WebDriver) -> (datetime.datetime, int):
    wait = __create_dynamic_data_waiter(driver)

    seoul_data = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'span.value'))
    )

    return datetime.datetime.now(), int(seoul_data.text)


def __check_not_have_to_get_data() -> bool:
    if get_date_last_yellow_dust() >= datetime.datetime.now() - datetime.timedelta(hours=1):
        return True
    else:
        return False
