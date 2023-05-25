from flask import Flask

from domain.update_data import update_data
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
    grade, mask = update_data()
    logger.info("getting data is done!")

    mask_string = ""
    if mask:
        mask_string = "True"
    else:
        mask_string = "False"

    return "grade : " + str(grade) + ", mask : " + mask_string


if __name__ == '__main__':
    app.run()
