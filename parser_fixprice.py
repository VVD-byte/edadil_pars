from parser import pars
import json
import logging
from bs4 import BeautifulSoup

class pars_fixprice(pars):
    def __init__(self):
        super().__init__()
        self.logger_fixprice = logging.getLogger(__name__)
        self.logger_fixprice.addHandler(logging.FileHandler('logs/fixprice.log'))
        self.city_id = {
            'Москва':'16375',
            'Санкт-Петербург':'16589',
            'Новосибирск':'16915',
            'Екатеринбург':'16680',
            'Казань':'16379',
            'Нижний Новгород':'16629',
            'Челябинск':'16272',
            'Самара':'16433',
            'Омск':'16913',
            'Ростов-на-Дону':'16342',
            'Уфа':'16746',
            'Красноярск':'17005',
            'Воронеж ':'16575',
            'Пермь':'16656',
            'Волгоград':'16883',
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        }
        self.cookies = {
            'CURRENT_LOCATION_ID':'',
        }
        self.url = 'https://fix-price.ru/catalog/'
        self.rub = {}
        self.magasine_date = {'id':16400, 'name': 'fix_price', 'original_logo_url':'', 'discount_count': 0}
        self.id_plus = 0

    def start_pars(self):
        try:
            if self.get_update_discounts_discount_company(self.magasine_date['name'])[0]:
                self.magasine_date['original_logo_url'] = self.get_soup('https://fix-price.ru/catalog/').find_all('img', {'class':'card-img'})[0].get('src')
                for i in self.city:
                    self.rub = {}
                    self.id_plus = self.city_id_all[i]
                    self.logger_fixprice.info(f'fixprice Выбран город {i}')
                    self.cookies['CURRENT_LOCATION_ID'] = self.city_id.get(i)
                    self.logger_fixprice.info(f'fixprice start parsing rubric {i}')
                    self.rubric()
                    self.logger_fixprice.info(f'fixprice start parsing tovar {i}')
                    self.pars_id_tovar()
                    self.add_discount_city_company(i, self.magasine_date['id'] + self.id_plus)
            if self.get_update_discount_filials(self.magasine_date['name']):
                self.magasine_date['discount_count'] = self.get_len_discount(self.magasine_date['id'])
                if not self.get_update_discounts_discount_company(self.magasine_date['name'])[1]:
                    self.add_data_discount_company(self.magasine_date)
                    self.logger_fixprice.info(f'fixprice {self.magasine_date["name"]} DB discount_company ADD')
                else:
                    print('update')
        except Exception as e:
            self.logger_fixprice.exception(f'Error start_pars fixprice')

    #парсит все рубрики и заполняет dict
    def rubric(self):
            soup = self.get_soup(self.url)
            for i in soup.find_all('li', {'class':'aside-list__item'}):
                self.rub[i.find('a').text] = {}
                for j in i.find_all('li', {'class':'aside-sublist__item'}):
                    self.rub[i.find('a').text][j.text.replace('  ', '').replace('\n', '')] = {}
                    self.rub[i.find('a').text][j.text.replace('  ', '').replace('\n', '')]['src'] = 'https://fix-price.ru' + j.find('a').get('href')
                if not self.rub[i.find('a').text]:
                    self.rub[i.find('a').text]['src'] = 'https://fix-price.ru' + i.find('a').get('href')
            self.add_discount_category(self.rub, self.magasine_date['id'])

    #парсит id всех товаров данной рубрики
    def pars_page(self, url, data):
        for i in range(1, self.get_max_page(url)):
            soup = self.get_soup(url + '?PAGEN_1=%s' %i)
            all_price = soup.find_all('span', {'style': 'font-family: RotondaC-Bold;'})
            all_img = soup.find_all('img', {'itemprop':'image'})
            for idd, j in enumerate(soup.find_all('a', {'class':'product-card__title'})):
                _id = int(j.get('href').split('/')[-2])
                data[_id] = {}
                data[_id]['original_id'] = _id
                data[_id]['original_url'] = 'https://fix-price.ru' + j.get('href')
                data[_id]['thumbnail_url'] = all_img[idd].get('src')
                data[_id]['product_name'] = j.text.replace('  ', '').replace('\r', '').replace('\n', '')
                data[_id]['adult'] = False
                data[_id]['price'] = str(int(float(all_price[idd].text.replace(',', '.')) * 100))
                data[_id]['original_company_id'] = self.magasine_date['id'] + self.id_plus

    def pars_data_product(self, data, *args, **kwargs):
        for i in data:
            if i != 'src':
                soup = self.get_soup(data[i]['original_url'])
                data[i]['description'] = soup.find('div', {'class':'tab__text'}).text
                self.logger_fixprice.info(f'fixprice ADD DATA {data[i]["product_name"]} - {data[i]["original_id"]} - {data[i]["original_company_id"]}')
                self.add_data_discount(data[i], *args, **kwargs)

    #просматривает рубрики и отправляет на парсинг
    def pars_id_tovar(self):
        for i, items in self.rub.items():
            self.logger_fixprice.info(f'fixprice Парсим "{i}"')
            if 'src' in items:
                self.pars_page(items['src'], self.rub[i])
                self.pars_data_product(self.rub[i], rubric1 = i, company_id = self.magasine_date['id'])
                self.rub[i] = {}
            else:
                for j, item in items.items():
                    self.logger_fixprice.info(f'fixprice Парсим {i} - {j}')
                    self.pars_page(item['src'], self.rub[i][j])
                    self.pars_data_product(self.rub[i][j], rubric1 = i, rubric2 = j, company_id = self.magasine_date['id'])
                    self.rub[i][j] = {}

    #смотрит количество страниц рубрики
    def get_max_page(self, url):
        try:
            return int(self.get_soup(url).find_all('li', {'class':'paging__item'})[-1].text)
        except:
            return 2

    def get_soup(self, url):
        a = self.requests_get(url, self.headers, cookies = self.cookies)
        if a:
            return BeautifulSoup(a, 'lxml')
        else:
            return False