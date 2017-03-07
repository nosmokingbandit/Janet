import logging
from logging.handlers import RotatingFileHandler
import os


logfile = os.path.join(os.getcwd(), 'janet.log')

formatter = logging.Formatter('%(levelname)s %(asctime)s %(funcName)s %(message)s')

handler = RotatingFileHandler(logfile, mode='a', maxBytes=5*1024*1024,
                              backupCount=1, encoding=None, delay=0)
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)
