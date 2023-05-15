from flask import Flask

from domain.covid import get as get_covid
from domain.air_quality import get as get_air_quality_pm10
from domain.air_quality import get as get_air_quality_pm25


app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    # get_covid.get()
    get_air_quality_pm10.get()
    get_air_quality_pm25.get()

    return 'Hello World!'


if __name__ == '__main__':
    app.run()
