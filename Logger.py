
import logging

from Config import LOG_LVL
from Config import LOG_FILE
from Config import LOG_FMT


class Logger:
    
    @classmethod
    def setup(cls, lvl: str = 'INFO', filename: str | None = None, format: str = '%(asctime)s %(levelname)s %(message)s'):
        if filename is not None:
            logging.basicConfig(level=cls.__lvl_by_name(lvl), filename=filename, filemode='w', format=format)
        else:
            logging.basicConfig(level=cls.__lvl_by_name(lvl), format=format)

    @classmethod
    def get(cls):
        return logging.getLogger()

    @classmethod
    def __lvl_by_name(cls, level: str):
        if level == 'DEBUG':
            return logging.DEBUG
        if level == 'INFO':
            return logging.INFO
        if level == 'WARNING':
            return logging.WARNING
        if level == 'ERROR':
            return logging.ERROR
        if level == 'CRITICAL':
            return logging.CRITICAL
        return logging.INFO


Logger.setup(LOG_LVL, LOG_FILE, LOG_FMT)
log = Logger.get()
