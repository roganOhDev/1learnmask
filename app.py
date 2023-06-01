import json
from flask import Flask, render_template, request

""" from domain.sensor.dust import get_dust_data_job """
""" from domain.sensor.ultra_sonic import ultra_sonic """
from domain.update_data import update_data, get_data
from utils.log import logger
from apscheduler.schedulers.background import BackgroundScheduler
from utils.updateschedule import job
import threading

app = Flask(__name__)

sched = BackgroundScheduler(daemon=True)
sched.add_job(job, 'cron', minute='5')
""" sched.add_job(get_dust_data_job, 'cron', minute='10') """
# sched.add_job(job, 'interval', seconds=40)

sched.start()

""" ultra_sonic_thread = threading.Thread(target=ultra_sonic)
ultra_sonic_thread.start() """

with app.app_context():    
    from domain import update_cache

    update_cache.run()


@app.route('/')
def hello_world():
    user_agent = request.user_agent.string
    
    covid_grade, pm10_grade, pm25_grade, yellow_dust_grade, cold_grade, grade, mask = update_data()
    logger.info("getting data is done!")

    covid_graph_data, air_quality_graph_data = get_data()
    response = {
        'grade': grade,
        'mask': mask,
        'covid_grade': covid_grade,
        'cold_grade': cold_grade,
        'pm10_grade': pm10_grade,
        'pm25_grade': pm25_grade,
        'yellow_dust_grade': yellow_dust_grade,
        'covid_graph_data': covid_graph_data,
        'air_quality_graph_data': air_quality_graph_data
    }
    if "Mobile" in user_agent or "Android" in user_agent:
        return render_template("mobile.html", data=json.dumps(response))
    else:
        return render_template('index.html', data=json.dumps(response))
    
@app.route('/mobile')
def helloo_world():
    user_agent = request.user_agent.string
    
    covid_grade, pm10_grade, pm25_grade, yellow_dust_grade, cold_grade, grade, mask = update_data()
    logger.info("getting data is done!(mobile)")

    covid_graph_data, air_quality_graph_data = get_data()
    response = {
        'grade': grade,
        'mask': mask,
        'covid_grade': covid_grade,
        'cold_grade': cold_grade,
        'pm10_grade': pm10_grade,
        'pm25_grade': pm25_grade,
        'yellow_dust_grade': yellow_dust_grade,
        'covid_graph_data': covid_graph_data,
        'air_quality_graph_data': air_quality_graph_data
    }
    return render_template("mobile.html", data=json.dumps(response))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9900, debug=True, use_reloader=False) #debug=True 는 실시간 html 변화 보려고 넣음.
