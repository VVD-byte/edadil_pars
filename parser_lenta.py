from parser import pars
from bs4 import BeautifulSoup
from db import DB

class pars_lenta(pars):
    def __init__(self):
        super().__init__()
        self.cookies = {
            "_ga": "GA1.2.1035808337.1605876331",
            "_gcl_au": "1.1.432327209.1605883098",
            "_gid": "GA1.2.617334113.1606133628",
            "_tm_lt_sid": "1605883100142.227595",
            "_ym_d": "1605883100",
            "_ym_isad": "1",
            "_ym_uid": "1605876331784480800",
            "lentaT2": "msk",
            "tmr_lvid": "3e47e430bf08d135d26bad0259bb6985",
            "tmr_lvidTS": "1605876331023",
            "tmr_reqNum": "382",
            ".ASPXANONYMOUS": "H-BFys-HdTa6WkcthkkIHSXTwP22AkiKHeANox-io8scp5E1go1n5uB0ovfLiFrrhQDiH-Rc4Ani_rlnSeRDN4OH8nGxYsUCO2LBtmPspYhA3UuT78tb6tYZm0FwDRSoujK4MQ2",
            "ASP.NET_SessionId": "heu1x0ugjxubkbchcjtkpmkp",
            "CityCookie": "msk",
            "CustomerId": "5426db0013594778a9fff587295e97cd",
            "KFP_DID": "041f6096-0fd7-5167-d86e-7518e7b07722",
            "oxxfgh": "aac7db98-31c2-4ea7-9aa3-ded2974f5946#0#1800000#5000",
            "ReviewedSkus": "455714",
            "Store": "0183",
            "tmr_detect": "1%7C1606134048258",
            "UseCookieNotification": "true",
        }
        self.headers = {
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
            'Content-Type':'application/json',
            'Host':'lenta.com',
            'Origin':'https://lenta.com',
            'Referer':'https://lenta.com/catalog/myaso-ptica-kolbasa/',
        }
        self.data = {
            'filters': [],
            'limit': 24,
            'nodeCode': 'gd6dd9b5e854cf23f28aa622863dd6913', #'gd6dd9b5e854cf23f28aa622863dd6913',
            'offset': 44,
            'sortingType': 'ByPriority',
            'tag': '',
            'typeSearch': 1,
            'updateFilters': True,
        }
        self.url = 'https://lenta.com/catalog/'
        self.url_api = 'https://lenta.com/api/v1/skus/list'
        self.return_data = {
            'name':'Лента',
        }

    def get_start_url(self):
        #soup = BeautifulSoup(self.requests_get(self.url, self.headers, cookies = self.cookies), 'lxml')
        print(self.requests_post(self.url_api, self.headers, self.data, self.cookies))

    #название магазина и его лого
    #город и его id

    #18+ или нет
    #описание товара
    #id продукта на сайте
    #ссылка на продукт
    #название товара
    #категория / подкатегория
    #изображение

    #если есть акция, дата начала и окончания
    #если действует акция, старая цена на продукт
    #цена товара в копейках
    #тип акции
    #цифровое значение акции
    #краткое опесание акции