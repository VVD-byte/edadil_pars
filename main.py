from parser_lenta import pars_lenta
from parser_yarche import pars_yarche
from parser_bristol import pars_bristol
from parser_fixprice import pars_fixprice
from parser_perecr import pars_perecr
from settings import *
import threading
import schedule
import datetime
import time
import logging.config
from db import DB

class start_pars:
    def __init__(self):
        logging.config.fileConfig('logs/docs/logging_main.ini', disable_existing_loggers=False)
        self.logger_main = logging.getLogger(__name__)

    def start(self):
        self.logger_main.info('start all')
        schedule.every(DAY_PARS_BRISTOL).day.at((datetime.timedelta(minutes = 1) + datetime.datetime.now()).strftime("%H:%M")).do(self.start_pars_bristol)
        self.logger_main.info('SCHEDULE ADD PARS_BRISTOL')
        schedule.every(DAY_PARS_YARCHE).day.at((datetime.timedelta(minutes = 1) + datetime.datetime.now()).strftime("%H:%M")).do(self.start_pars_yarche)
        self.logger_main.info('SCHEDULE ADD PARS_YARCHE')
        schedule.every(DAY_PARS_FIXPRICE).day.at((datetime.timedelta(minutes = 1) + datetime.datetime.now()).strftime("%H:%M")).do(self.start_pars_fixprice)
        self.logger_main.info('SCHEDULE ADD PARS_FIXPRICE')
        schedule.every(DAY_PARS_PERECT).day.at((datetime.timedelta(minutes=1) + datetime.datetime.now()).strftime("%H:%M")).do(self.start_pars_perecr)
        self.logger_main.info('SCHEDULE ADD PARS_PERECRESTOK')
        schedule.every(DAY_PARS_LENTA).day.at((datetime.timedelta(minutes=1) + datetime.datetime.now()).strftime("%H:%M")).do(self.start_pars_lenta)
        self.logger_main.info('SCHEDULE ADD PARS_LENTA')
        while True:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as e:
                self.logger_main.exception("Error start_while")

    def start_pars_bristol(self):
        try:
            t = datetime.datetime.now()
            a = pars_bristol()
            x = threading.Thread(target = a.start_pars)
            self.logger_main.info('START PARS_BRISTOL')
            x.start()
            x.join()
            DB().remove_removed(a.magasine_date['id'])
            print(datetime.datetime.now() - t, 'bristol')
        except Exception as e:
            self.logger_main.exception("Error start_pars_bristol")

    def start_pars_fixprice(self):
        try:
            t = datetime.datetime.now()
            a = pars_fixprice()
            x = threading.Thread(target = a.start_pars)
            self.logger_main.info("START PARS_FIXPRICE")
            x.start()
            x.join()
            DB().remove_removed(a.magasine_date['id'])
            print(datetime.datetime.now() - t, 'fixprice')
        except Exception as e:
            self.logger_main.exception("Error start_pars_yarche")

    def start_pars_perecr(self):
        try:
            t = datetime.datetime.now()
            a = pars_perecr()
            x = threading.Thread(target = a.start_pars)
            self.logger_main.info("START PARS_PERECRESTOK")
            x.start()
            x.join()
            DB().remove_removed(a.magasine_date['id'])
            print(datetime.datetime.now() - t, 'perecr')
        except Exception as e:
            self.logger_main.exception("Error start_pars_yarche")

    def start_pars_yarche(self):
        try:
            t = datetime.datetime.now()
            a = pars_yarche()
            x = threading.Thread(target = a.start_pars)
            self.logger_main.info("START PARS_YARCHE")
            x.start()
            x.join()
            DB().remove_removed(a.magasine_date['id'])
            print(datetime.datetime.now() - t, 'yarche')
        except Exception as e:
            self.logger_main.exception("Error start_pars_yarche")

    def start_pars_lenta(self):
        try:
            t = datetime.datetime.now()
            a = pars_lenta()
            x = threading.Thread(target = a.start_pars)
            self.logger_main.info("START PARS_LENTA")
            x.start()
            x.join()
            DB().remove_removed(a.magasine_date['id'])
            print(datetime.datetime.now() - t, 'lenta')
        except Exception as e:
            self.logger_main.exception("Error start_pars_lenta")

def main():
    DB().clear_all()
    a = start_pars()
    a.start()

if __name__ == '__main__':
    main()