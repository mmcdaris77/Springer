import logging
from logging.handlers import RotatingFileHandler
import os


me_dir = os.path.dirname(os.path.realpath(__file__))
LOGGING_PATH = os.path.join(os.path.dirname(me_dir), 'log\\log.log')

def logger(log_debug: bool = False):

    if log_debug:
        file_log_level = logging.DEBUG
    else:
        file_log_level = logging.INFO

    if not os.path.isdir(os.path.dirname(LOGGING_PATH)):
        os.mkdir(os.path.dirname(LOGGING_PATH))

    logger = logging.getLogger('lot_logger')
    logger.setLevel(file_log_level)

    # console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # file
    file_handler = RotatingFileHandler(LOGGING_PATH, maxBytes=5000000, backupCount=5)
    file_handler.setLevel(file_log_level)
    file_format = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    return logger








