import requests
from bs4 import BeautifulSoup
import json
from db import DB
from error import Status_code_error
import logging

class pars(DB):
    def __init__(self):
        super().__init__()
        self.logger_parser = logging.getLogger(__name__)
        self.logger_parser.addHandler(logging.FileHandler('logs/parser.log'))
        self.city_id_all = {
            'Москва': 1,
            'Санкт-Петербург': 2,
            'Новосибирск': 3,
            'Екатеринбург': 4,
            'Казань': 5,
            'Нижний Новгород': 6,
            'Челябинск': 7,
            'Самара': 8,
            'Омск': 9,
            'Ростов-на-Дону': 10,
            'Уфа': 11,
            'Красноярск': 12,
            'Воронеж ': 13,
            'Пермь': 14,
            'Волгоград': 15,
        }

    def requests_get(self, _url, head, dat = {}, cookies = {}):
        a = requests.get(_url, headers = head, data = dat, cookies = cookies)
        if a.status_code == 200:
            self.logger_parser.info(f'REQUESTS GET {a.status_code} - {_url}')
            return a.text
        else:
            self.logger_parser.info(f'ERROR REQUESTS GET {a.status_code} - {_url}')
            return False

    def requests_post(self, _url, head, dat = {}, cookies = {}):
        a = requests.post(_url, headers = head, data = dat, cookies = cookies)
        if a.status_code == 200:
            self.logger_parser.info(f'REQUESTS POST {a.status_code} - {_url}')
            return json.loads(a.text)
        else:
            self.logger_parser.info(f'ERROR REQUESTS POST {a.status_code} - {_url}')
            return False