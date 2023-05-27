import json

from flask import Flask

from domain.update_data import update_data, get_data
from utils.log import logger
from apscheduler.schedulers.background import BackgroundScheduler
from utils.updateschedule import job

app = Flask(__name__)

sched = BackgroundScheduler(daemon=True)

sched.add_job(job, 'cron', minute='5')
# sched.add_job(job, 'interval', seconds=30)

sched.start()

with app.app_context():
    from domain import update_cache

    update_cache.run()


@app.route('/')
def hello_world():  # put application's code here
    cold_grade, pm10_grade, pm25_grade, yellow_dust_grade, cold_grade, grade, mask = update_data()
    logger.info("getting data is done!")

    covid_graph_data, air_quality_graph_data = get_data()

    response = json.dumps(
        {'grade': grade, 'mask': mask, 'cold_grade': cold_grade, 'pm10_grade': pm10_grade, 'pm25_grade': pm25_grade,
         'yellow_dust_grade': yellow_dust_grade, 'cold_grade': cold_grade, 'covid_graph_data': covid_graph_data,
         'air_quality_graph_data': air_quality_graph_data})
    return response


if __name__ == '__main__':
    app.run()
