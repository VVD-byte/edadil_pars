import requests
from bs4 import BeautifulSoup
import json
from db import DB

class pars(DB):
    def __init__(self):
        super().__init__()

    @staticmethod
    def requests_get(_url, head, dat = {}, cookies = {}):
        a = requests.get(_url, headers = head, data = dat, cookies = cookies)
        if a.status_code == 200:
            return a.text
        else:
            assert f'ERROR requests_get status_code = {a.status_code}, url = {_url}'

    @staticmethod
    def requests_post(_url, head, dat = {}, cookies = {}):
        a = requests.post(_url, headers = head, data = dat, cookies = cookies)
        if a.status_code == 200:
            return json.loads(a.text)
        else:
            print(a.text)
            assert f'ERROR requests_get status_code = {a.status_code}, url = {_url}'