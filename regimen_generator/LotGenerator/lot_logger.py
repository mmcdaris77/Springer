import logging
from logging.handlers import RotatingFileHandler
import os

me_dir = os.path.dirname(os.path.realpath(__file__))
logging_path = os.path.join(os.path.dirname(me_dir), 'log\\log.log')

if not os.path.isdir(os.path.dirname(logging_path)):
    os.mkdir(os.path.dirname(logging_path))


logger = logging.Logger('lot_logger')

# handlers
console_handler = logging.StreamHandler()
file_handler = RotatingFileHandler(logging_path, maxBytes=5000000, backupCount=5)
console_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.DEBUG)

# formatters
console_format = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
file_format = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
console_handler.setFormatter(console_format)
file_handler.setFormatter(file_format)

# add to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)








