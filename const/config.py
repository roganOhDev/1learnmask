import os
from enum import Enum
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

# database
db_name = "data.db"


# version = RunVersion.debug
class RunVersion(Enum):
    debug = "DEBUG"
    demo = "DEMO"


version = RunVersion.demo

# arduino
# port = "COM3"
# port = "/dev/cu.Bluetooth-Incoming-Port"
# port_for_ultra_sonic = "/dev/cu.usbmodem1101"
port_for_ultra_sonic = "/dev/cu.usbserial-10"
baudrate = 9600
timeout = 2

# chrome driver
current_dir = os.path.dirname(os.path.abspath(__file__))
driver_path = os.path.join(current_dir, '../chromedriver/chromedriver')

service = Service(driver_path)
options = Options()
options.add_argument('--headless')
chrome_driver = webdriver.Chrome(service=service, options=options)

covid_url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%BD%94%EB%A1%9C%EB%82%98"
yellow_dust_url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%ED%99%A9%EC%82%AC"

cold_seongbuk_gu_code = 11290
