from parser import pars
from bs4 import BeautifulSoup
import json
import logging

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
        self.cit = 'Москва'

    def start_pars(self):
        for i in self.city:
            self.cit = i
            logging.info(f'Выбран город {i}')
            self.cookies['CURRENT_LOCATION_ID'] = self.city_id[i]
            self.rubric()
            logging.info(f'Собраны все рубрики города {i}')
            self.pars_id_tovar()
            break

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

    #парсит id всех товаров данной рубрики
    def pars_page(self, url, data):
        for i in range(1, self.get_max_page(url))[:1]:
            soup = self.get_soup(url + '?PAGEN_1=%s' %i)
            all_price = soup.find_all('span', {'style': 'font-family: RotondaC-Bold;'})
            all_img = soup.find_all('img', {'itemprop':'image'})
            for idd, j in enumerate(soup.find_all('a', {'class':'product-card__title'})):
                _id = int(j.get('href').split('/')[-2])
                data[_id] = {}
                data[_id]['src'] = 'https://fix-price.ru' + j.get('href')
                data[_id]['img_src'] = all_img[idd].get('src')
                data[_id]['name'] = j.text.replace('  ', '').replace('\r', '').replace('\n', '')
                data[_id]['price'] = all_price[idd].text
                data[_id]['years'] = ''
                try:
                    data[_id]['price_copey'] = str(int(all_price[idd].text) * 60)
                except: data[_id]['price_copey'] = int(float(all_price[idd].text.replace(',', '.'))//1 * 60 + float(all_price[idd].text.replace(',', '.'))%1 * 60)

    def pars_data_product(self, data, *args, **kwargs):
        for i in data:
            if i != 'src':
                soup = self.get_soup(data[i]['src'])
                data[i]['opisanie'] = soup.find('div', {'class':'tab__text'})
                self.add_data(data.pop(i), *args)

    #просматривает рубрики и отправляет на парсинг
    def pars_id_tovar(self):
        for i, items in self.rub.items():
            logging.info(f'Парсим "{i}"')
            if 'src' in items:
                self.pars_page(items['src'], self.rub[i])
                self.pars_data_product(self.rub[i], i)
            else:
                for j, item in items.items():
                    logging.info(f'Парсим {i} - {j}')
                    self.pars_page(item['src'], self.rub[i][j])
                    self.pars_data_product(self.rub[i][j], i, j)
        with open('prod.json', 'w') as t: t.write(json.dumps(self.rub).encode('cp1251').decode('unicode-escape'))
        logging.info('ЗАПИСЬ ПРОШЛА УСПЕШНО')

    #смотрит количество страниц рубрики
    def get_max_page(self, url):
        try:
            return int(self.get_soup(url).find_all('li', {'class':'paging__item'})[-1].text)
        except:
            return 2

    def get_soup(self, url):
        a = self.requests_get(url, self.headers, cookies = self.cookies)
        return BeautifulSoup(a, 'lxml')