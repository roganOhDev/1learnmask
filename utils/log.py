import logging

from colorlog import ColoredFormatter

logger = logging.getLogger()

logger.setLevel(logging.INFO)

formatter = ColoredFormatter('%(asctime)s - %(log_color)s%(levelname)s%(reset)s - %(blue)s%(message)s',
                             log_colors={
                                 'DEBUG': 'cyan',
                                 'INFO': 'green',
                                 'WARNING': 'yellow',
                                 'ERROR': 'red',
                                 'CRITICAL': 'red,bg_white',
                             },
                             )

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

logging.getLogger('sqlalchemy').setLevel(logging.ERROR)
