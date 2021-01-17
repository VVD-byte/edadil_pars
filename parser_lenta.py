from parser import pars
from bs4 import BeautifulSoup
from db import DB
import logging.config
import json

class pars_lenta(pars):
    def __init__(self):
        super().__init__()
        logging.config.fileConfig('logs/docs/logging_bristol.ini', disable_existing_loggers=False)
        self.logger_lenta = logging.getLogger(__name__)
        self.city_id = {
            'Москва': 'msk',
            'Санкт-Петербург': 'spb',
            'Новосибирск': 'nsk',
            'Екатеринбург': 'ekat',
            'Казань': 'kazan',
            'Нижний Новгород': 'nnvgrd',
            'Челябинск': 'chlb',
            'Самара': 'smr',
            'Омск': 'omsk',
            'Ростов-на-Дону': 'rnd',
            'Уфа': 'ufa',
            'Красноярск': 'krsn',
            'Воронеж ': 'vrn',
            'Пермь': 'prm',
            'Волгоград': 'vlg',
        }
        self.cookies = {
            "lentaT2": "msk",
            'CityCookie': 'msk',
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36}'
        }
        self.url = 'https://lenta.com/catalog/'
        self.url_api = 'https://lenta.com/api/v1/skus/list'
        self.rub = {}
        self.magasine_date = {'id': 16700, 'name': 'lenta', 'original_logo_url': '', 'discount_count': 0}
        self.id_plus = 0
        self.data = {
            'filters': [],
            'limit': 1000,
            'nodeCode': "cf0349a2de3bac83f8d359ff8b960c798",
            'offset': 0,
            'pricesRange': 'null',
            'sortingType': "ByPriority",
            'tag': "",
            'typeSearch': 1,
            'updateFilters': True,
        }

    def start_pars(self):
        try:
            if self.get_update_discounts_discount_company(self.magasine_date['name'])[0]:
                self.magasine_date['original_logo_url'] = self.get_soup('https://lenta.com/catalog/').find('a', {'class':'header__logo'}).find('img').get('src')
                for i in self.city[:1]:     ###########################
                    self.rub = {}
                    if i in self.city_id:
                        self.id_plus = self.city_id_all[i]
                        self.logger_lenta.info(f'lenta Выбран город {i}')
                        self.cookies['lentaT2'] = self.city_id[i]
                        self.cookies['CityCookie'] = self.city_id[i]
                        self.logger_lenta.info(f'lenta start parsing rubric {i}')
                        self.rubric()
                        self.logger_lenta.info(f'lenta start parsing tovar {i}')
                        self.pars_id_tovar()
                        self.add_discount_city_company(i, self.magasine_date['id'] + self.id_plus)
            if self.get_update_discount_filials(self.magasine_date['name']):
                self.magasine_date['discount_count'] = self.get_len_discount(self.magasine_date['id'])
                if not self.get_update_discounts_discount_company(self.magasine_date['name'])[1]:
                    self.add_data_discount_company(self.magasine_date)
                    self.logger_lenta.info(f'lenta {self.magasine_date["name"]} DB discount_company ADD')
        except Exception as e:
            self.logger_lenta.exception(f'Error start_pars lenta')
        self.logger_lenta.info("END PARS lenta")
        print(f"end {self.magasine_date['name']}")

    def rubric(self):
        json_ = json.loads(self.get_soup(self.url).find('div', {'class':'header__catalog-menu-container'}).get('data-menu'))
        for i in json_['groups']:       ########################
            self.rub[i['name']] = {}
            for j in i['childNodes']:
                self.rub[i['name']][j['name']] = {}
                for q in j['childNodes']:
                    self.rub[i['name']][j['name']][q['name']] = {'code':q['code'],
                                                                 'src':'hpps://'######не убирать ни в коем случае!!!!
                                                                 }
        self.add_discount_category(self.rub, self.magasine_date['id'])

    def pars_id_tovar(self, *args, **kwargs):
        for w in self.rub:
            for j in self.rub[w]:
                for q in self.rub[w][j]:
                    self.data['nodeCode'] = self.rub[w][j][q]['code']
                    for i in self.requests_post(self.url_api, self.headers, self.data, self.cookies)['skus']:
                        data = {}
                        data['original_url'] = 'https://lenta.com' + i['skuUrl']
                        data['original_id'] = i['code']
                        data['adult'] = False
                        data['thumbnail_url'] = i['imageUrl']
                        data['product_name'] = i['title']
                        if '9999' not in i['promoEnd']:
                            data['price'] = int(float(i['cardPrice']['value']) * 100)
                            data['old_price_note'] = i['regularPrice']['value']
                            data['promo_type'] = 'PERCENT'
                            data['promo_sort_hint'] = i['promoPercent']
                            data['promo_str'] = f'{data["promo_sort_hint"]}%'
                        else: data['price'] = int(float(i['regularPrice']['value']) * 100)
                        data['description'] = i['description']
                        if i['isWeightProduct']: data['value_note'] = '₽/кг'
                        else: data['value_note'] = '₽/шт'
                        data['original_company_id'] = self.magasine_date['id'] + self.id_plus
                        self.add_data_discount(data, company_id = self.magasine_date['id'], rubric1=w, rubric2=j, rubric3=q, *args, **kwargs)

    def clear_text(self, text):
        return text.replace('  ', '').replace('\n', '').replace('\r', '')

    def get_soup(self, url):
        a = self.requests_get(url, self.headers, cookies = self.cookies)
        if a:
            return BeautifulSoup(a, 'lxml')
        else:
            return False

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

if __name__ == "__main__":
    a = pars_lenta()
    a.start_pars()