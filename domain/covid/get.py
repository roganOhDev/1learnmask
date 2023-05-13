import datetime
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

current_dir = os.path.dirname(os.path.abspath(__file__))
driver_path = os.path.join(current_dir, './chromedriver/chromedriver')
service = Service(driver_path)  # Replace 'path/to/chromedriver' with the actual path to your ChromeDriver executable
options = Options()
options.add_argument('--headless')  # Optional: Run Chrome in headless mode to perform the crawling silently
driver = webdriver.Chrome(service=service, options=options)

url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%BD%94%EB%A1%9C%EB%82%98"

# Navigate to the URL
driver.get(url)

# Find the elements that contain the data you want to extract
element = driver.find_element(By.CSS_SELECTOR,
                              "div._infect_content[data-type='status'][data-param='u1=1'][style='display: block;']")

wait = WebDriverWait(element, 10)

graph = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'dl.data_content.-bar_thin.-bar_data._x_axis_and_series_label'))
)

elements = graph.find_elements(By.CSS_SELECTOR, "div.column._column")
date_string = elements[0].find_element(By.CSS_SELECTOR, "dt.x_axis_value").text
first_day = datetime.date(datetime.datetime.now().year, int(date_string.split('.')[0]), int(date_string.split('.')[1]))

values = []
dates = []

for element_ in elements:
    span = element_.find_element(By.CSS_SELECTOR, "span.text")
    value = span.get_attribute('innerText')

    value = value.replace(',', '').replace('최저', '').replace('최고', '').strip()

    if dates.__len__() == 0:
        dates.append(first_day)
    else:
        dates.append(dates[-1] + datetime.timedelta(days=1))

    values.append(int(value))

driver.quit()

pairs = list(zip(dates, values))
for pair in pairs:
    print(pair)
