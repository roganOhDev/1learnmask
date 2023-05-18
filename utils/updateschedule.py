from domain.update_data import update_data
from utils.log import logger


def job():
    update_data()
    logger.info("Data update is executed on :05")
