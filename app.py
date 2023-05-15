from flask import Flask

from domain.covid import get as get_covid
from domain.air_quality import get as get_air_quality_pm10
from domain.air_quality import get as get_air_quality_pm25
from utils.log import logger

app = Flask(__name__)

with app.app_context():
    from domain import update_cache

    update_cache.run()


@app.route('/')
def hello_world():  # put application's code here
    get_covid.get()
    get_air_quality_pm10.get()
    get_air_quality_pm25.get()
    logger.info("getting data is done!")

    return 'Hello World!'


if __name__ == '__main__':
    app.run()
