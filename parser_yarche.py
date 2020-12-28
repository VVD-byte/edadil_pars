import json
from parser import pars
import logging
from bs4 import BeautifulSoup
from requests import ConnectionError

logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class pars_yarche(pars):
    def __init__(self):
        super().__init__()
        self.data_yarce = {
            'query': "query ($categoryId: Int!, $filter: [FilterInput], $sort: SortInput, $pagination: PageInput) {    products (categoryId: $categoryId, filter: $filter, sort: $sort, page: $pagination) {      list {  id  name  description  amount  image {  id  title  alt}  price  previousPrice  itemSum  isNew  isHit  isFavorite  isAvailable  isSubscribed  isVeterinaryControl  code  quant {  code  fullName  shortName  multiple  pricePerUnit  previousPricePerUnit  unit  type  minAmount  stepAmount}  categories {  id  name  code  treeId  parentTreeId}}      page {  total  limit  page}      filter {  id  type  name  title  options {  id  value  label  count  isApplied}}      sort {  param  title  direct  isApplied}    }  }",
            'variables': {
                "categoryId": 0,
                "pagination": {
                    "page": 1,
                    "limit": 100
                }
            }
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        }
        self.url = 'https://yarcheplus.ru/category'
        self.rub = {}
        self.magasine_date = {'id': 16401, 'name': 'fix_price', 'original_logo_url': '', 'discount_count': 0}

    def start_pars(self):
        if self.get_update_discounts_discount_company(self.magasine_date['name'])[0]:
            self.magasine_date['original_logo_url'] = '' ############################################   исправить
            logging.info('start parsing rubric')
            self.rubric()
            logging.info('start parsing tovar')
            self.pars_id_tovar()

    def rubric(self):
        try:
            for i in self.get_soup(self.url).find_all('a', {'class':'a3Qfg-QHM b3Qfg-QHM'}):
                if self.clear_soup_text(i) != '':
                    self.rub[self.clear_soup_text(i)] = {}
                    for j in self.get_soup('https://yarcheplus.ru' + i.get('href')).find_all('a', {'class':'a3Qfg-QHM b3Qfg-QHM'}):
                        if self.clear_soup_text(j) != '':
                            self.rub[self.clear_soup_text(i)][self.clear_soup_text(j)] = {'src':'https://yarcheplus.ru' + j.get('href')}
                    if self.rub[self.clear_soup_text(i)] == {}:
                        self.rub[self.clear_soup_text(i)]['src'] = 'https://yarcheplus.ru' + i.get('href')
                    a = 1/0         ################################################
        except ConnectionError as e:
            print(e)
        except:         #################################################
            print(10)    ############################################
        self.clear_all_category()  ################################################
        self.add_discount_category(self.rub, self.magasine_date['id'])

    def pars_id_tovar(self):
        for i, items in self.rub.items():
            if 'src' in items:
                logging.info(f'start parsing_ {i}')
                self.get_page_tovar(items)
                self.get_tovar(items, rubric1 = i, company_id = self.magasine_date['id'])
                self.write_file()
                self.rub[i] = {}
            else:
                for j, item in items.items():
                    if 'src' in item:
                        logging.info(f'start parsing {j}')
                        self.get_page_tovar(item)
                        self.get_tovar(item, rubric1 = i, rubric2 = j, company_id = self.magasine_date['id'])
                        self.write_file()
                        self.rub[i][j] = {}
            break

    def write_file(self):
        with open('q.json', 'w', encoding = 'utf-8') as t:
            t.write(json.dumps(self.rub, ensure_ascii = False))
        a = 1/0 #############################

    def get_page_tovar(self, data):
        for i in range(1, self.get_len_page(data['src'])):
            for j in self.get_soup(data['src'] + f'?page={i}').find_all('div', {'class':'c3s8K6a5X'}):
                name = j.find('a', {'class':'f2mGXj5-x'}).get('href').split('/')[-1]
                data[name] = {}
                data[name]['original_id'] = name
                data[name]['original_url'] = 'https://yarcheplus.ru' + j.find('a', {'class':'f2mGXj5-x'}).get('href')
                data[name]['thumbnail_url'] = j.find('img', {'class':'k2mGXj5-x'}).get('src')
                data[name]['product_name'] = j.find('a', {'class':'f2mGXj5-x'}).text
                data[name]['price'] = j.find('div', {'class':'a34tOzx2Q'}).text.replace(' ', '').replace('₽', '')
                data[name]['adult'] = False #################################b'0'
                data[name]['value_note'] = j.find('div', {'class':'b34tOzx2Q'}).text
                data[name]['price_copey'] = str(int(float(data[name]['price'].replace(',', '.')) * 100))

    def get_len_page(self, url):
        try:
            return int(self.get_soup(url).find_all('a', {'class':'b18ybbMcB'})[-2])
        except:
            return 2

    def get_soup(self, url):
        a = self.requests_get(url, self.headers)
        return BeautifulSoup(a, 'lxml')

    def get_tovar(self, data, *args, **kwargs):
        for i, items in data.items():
            if i != 'src':
                dat = self.get_soup(items.get('original_url', ''))
                items['description'] = dat.find('div', {'class':'fa3QZxpOf a2Q0qeMRL d2Q0qeMRL'}).text
                ###self.add_data_discount(items, *args, **kwargs)

    @staticmethod
    def clear_soup_text(text):
        return text.text.replace('  ', '').replace('\n', '')