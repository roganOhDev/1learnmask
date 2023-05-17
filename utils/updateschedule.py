from utils.log import logger
from domain.covid import get as get_covid
from domain.air_quality import get as get_air_quality_pm10
from domain.air_quality import get as get_air_quality_pm25


def job():
    get_covid.get()
    get_air_quality_pm10.get()
    get_air_quality_pm25.get()
    logger.info("Data update is executed on :05")
