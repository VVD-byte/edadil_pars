from parser import pars
import json
import logging
from bs4 import BeautifulSoup

logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class pars_fixprice(pars):
    def __init__(self):
        super().__init__()
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
        self.data = {
            'name':'fix_price',
            'city':{
            }
        }
        self.url = 'https://fix-price.ru/catalog/'
        self.rub = {}
        self.magasine_date = {'id':16400, 'name': 'fix_price', 'original_logo_url':'', 'discount_count': 0}

    def start_pars(self):
        if self.get_update_discounts_discount_company(self.magasine_date['name'])[0]:
            self.magasine_date['original_logo_url'] = self.get_soup('https://fix-price.ru/catalog/').find_all('img', {'class':'card-img'})[0].get('src')
            for i in self.city:
                logging.info(f'Выбран город {i}')
                self.cookies['CURRENT_LOCATION_ID'] = self.city_id[i]
                self.rubric()
                logging.info(f'Собраны все рубрики города {i}')
                self.pars_id_tovar()
                break                       ##########################################################
            self.magasine_date['discount_count'] = self.get_len_discount(self.magasine_date['id'])
            if not self.get_update_discounts_discount_company(self.magasine_date['name'])[1]:
                self.add_data_discount_company(self.magasine_date)
                logging.info(f'{self.magasine_date["name"]} DB discount_company ADD')
            else:
                print('update')

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
                break           #######################################################
            self.clear_all_category()  ################################################
            self.add_discount_category(self.rub, self.magasine_date['id'])

    #парсит id всех товаров данной рубрики
    def pars_page(self, url, data):
        for i in range(1, self.get_max_page(url))[:1]:  ############################################ [:1]
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
                data[_id]['price'] = all_price[idd].text
                data[_id]['adult'] = b'0'
                data[_id]['price_copey'] = str(int(float(all_price[idd].text.replace(',', '.')) * 100))

    def pars_data_product(self, data, *args, **kwargs):
        for i in data:
            if i != 'src':
                soup = self.get_soup(data[i]['original_url'])
                data[i]['description'] = soup.find('div', {'class':'tab__text'}).text
                logging.info(f'{self.magasine_date["name"]} DB discount ADD {i}')
                self.add_data_discount(data[i], *args, **kwargs)

    #просматривает рубрики и отправляет на парсинг
    def pars_id_tovar(self):
        self.clear_all_discount()                   ###########################################
        for i, items in self.rub.items():
            logging.info(f'Парсим "{i}"')
            if 'src' in items:
                self.pars_page(items['src'], self.rub[i])
                self.pars_data_product(self.rub[i], rubric1 = i, company_id = self.magasine_date['id'])
                self.rub[i] = {}
            else:
                for j, item in items.items():
                    logging.info(f'Парсим {i} - {j}')
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
        return BeautifulSoup(a, 'lxml')