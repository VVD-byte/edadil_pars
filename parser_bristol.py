from parser import pars
import json
import logging
from bs4 import BeautifulSoup

logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class pars_bristol(pars):
    def __init__(self):
        super().__init__()
        self.url = 'https://bristol.ru/catalog/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        }
        self.magasine_date = {'id': 16402, 'name': 'bristol', 'original_logo_url': '', 'discount_count': 0}
        self.rub = {}

    def start_pars(self):
        if self.get_update_discounts_discount_company(self.magasine_date['name'])[0]:
            self.magasine_date['original_logo_url'] = 'https://bristol.ru/local/templates/bristol/images/logo.svg'
            logging.info('start parsing rubric')
            self.rubric()
            logging.info('start parsing tovar')
            self.pars_id_tovar()

    #ссылки рубрик
    def rubric(self):
        for i in self.get_soup(self.url).find_all('a', {'class':'bx_catalog_tile_img'}):
            self.rub[i.find('h2').text] = {'src':'https://bristol.ru' + i.get('href')}
            logging.info(i.find('h2').text)
        self.add_discount_category(self.rub, self.magasine_date['id'])

    #id всех товаров
    def pars_id_tovar(self):
        for i, items in self.rub.items():
            logging.info(f'start parsing {i}')
            for j in range(self.get_count_page(items['src']))[:2]:          ##########################убрать [:2]
                for q in self.get_soup(f'{items["src"]}?PAGEN_1={j}').find_all('a', {'class':'link'}):
                    self.pars_data({'id':int(q.get('id').split('_')[-2]), 'src':f"https://bristol.ru{q.get('href')}"})
            self.write_file()

    def pars_data(self, data):
        pass

    def get_count_page(self, url):
        return int(self.get_soup(url).find_all('div', {'class':'btn pag-btn'})[-1].text.replace('\n', ''))

    def get_soup(self, url):
        a = self.requests_get(url, self.headers)
        return BeautifulSoup(a, 'lxml')

    def write_file(self):
        with open('q.json', 'w', encoding = 'utf-8') as t:
            t.write(json.dumps(self.rub, ensure_ascii = False))
        a = 1/0 #############################

    def write_files(self, a):
        with open('q.txt', 'w', encoding = 'utf-8') as t:
            t.write(a)
        a = 1/0 #############################