from parser import pars
import json
import logging.config
from bs4 import BeautifulSoup

class pars_bristol(pars):
    def __init__(self):
        super().__init__()
        logging.config.fileConfig('logs/docs/logging_bristol.ini', disable_existing_loggers=False)
        self.logger_bristol = logging.getLogger(__name__)

        self.url = 'https://bristol.ru/catalog/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        }
        PHP_SESS = 'tb20ub5eahsi02uavakadkj58v'
        self.city_id = {
            'Москва': {
                'STORE_ID':'5246',
                'ADDRESS':'+%D0%97%D0%B5%D0%BB%D0%B5%D0%BD%D0%BE%D0%B3%D1%80%D0%B0%D0%B4%D1%81%D0%BA%D0%B0%D1%8F+%D1%83%D0%BB%2C+%D0%B4%D0%BE%D0%BC+%E2%84%96+31%2C+%D0%BA%D0%BE%D1%80%D0%BF%D1%83%D1%81+1',
                'CITY':'%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0',
                'REGION':'%D0%9C%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F',
                'PHPSESSID':PHP_SESS,
            },
            'Санкт-Петербург': {
                'STORE_ID':'4539',
                'ADDRESS':'+%D0%91%D0%B5%D0%BB%D1%8B+%D0%9A%D1%83%D0%BD%D0%B0+%D1%83%D0%BB%2C+%D0%B4%D0%BE%D0%BC+%E2%84%96+6%2C+%D0%BA%D0%BE%D1%80%D0%BF%D1%83%D1%81+1',
                'CITY':'%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3',
                'REGION':'%D0%9B%D0%B5%D0%BD%D0%B8%D0%BD%D0%B3%D1%80%D0%B0%D0%B4%D1%81%D0%BA%D0%B0%D1%8F',
                'PHPSESSID':PHP_SESS,
            },
            'Новосибирск': {
                'STORE_ID':'5914',
                'ADDRESS':'%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA',
                'CITY':'%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA',
                'REGION':'%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%D0%B0%D1%8F',
                'PHPSESSID':PHP_SESS,
            },
            'Екатеринбург': {
                'STORE_ID':'4196',
                'ADDRESS':'8+%D0%9C%D0%B0%D1%80%D1%82%D0%B0+%D1%83%D0%BB%2C+%D0%B4%D0%BE%D0%BC+%E2%84%96+128',
                'CITY':'%D0%95%D0%BA%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%BD%D0%B1%D1%83%D1%80%D0%B3',
                'REGION':'%D0%A1%D0%B2%D0%B5%D1%80%D0%B4%D0%BB%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F',
                'PHPSESSID':PHP_SESS,
            },
            'Казань': {
                'STORE_ID':'5262',
                'ADDRESS':'%D0%90%D0%BA%D0%B0%D0%B4%D0%B5%D0%BC%D0%B8%D0%BA%D0%B0+%D0%A1%D0%B0%D1%85%D0%B0%D1%80%D0%BE%D0%B2%D0%B0+%D1%83%D0%BB%2C+%D0%B4%D0%BE%D0%BC+%E2%84%96+31%D0%94',
                'CITY':'%D0%9A%D0%B0%D0%B7%D0%B0%D0%BD%D1%8C',
                'REGION':'%D0%A2%D0%B0%D1%82%D0%B0%D1%80%D1%81%D1%82%D0%B0%D0%BD',
                'PHPSESSID':PHP_SESS,
            },
            'Нижний Новгород': {
                'STORE_ID':'1143',
                'ADDRESS':'40+%D0%BB%D0%B5%D1%82+%D0%9F%D0%BE%D0%B1%D0%B5%D0%B4%D1%8B+%D1%83%D0%BB%2C+%D0%B4%D0%BE%D0%BC+%E2%84%96+18',
                'CITY':'%D0%9D%D0%B8%D0%B6%D0%BD%D0%B8%D0%B9+%D0%9D%D0%BE%D0%B2%D0%B3%D0%BE%D1%80%D0%BE%D0%B4',
                'REGION':'%D0%9D%D0%B8%D0%B6%D0%B5%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D1%81%D0%BA%D0%B0%D1%8F',
                'PHPSESSID':PHP_SESS,
            },
            'Самара': {
                'STORE_ID':'1665',
                'ADDRESS':'%D0%90%D0%B2%D1%80%D0%BE%D1%80%D1%8B+%D1%83%D0%BB%2C+%D0%B4%D0%BE%D0%BC+%E2%84%96+219',
                'CITY':'%D0%A1%D0%B0%D0%BC%D0%B0%D1%80%D0%B0',
                'REGION':'%D0%A1%D0%B0%D0%BC%D0%B0%D1%80%D1%81%D0%BA%D0%B0%D1%8F',
                'PHPSESSID':PHP_SESS,
            },
            'Омск': {
                'STORE_ID':'1350',
                'ADDRESS':'22+%D0%9F%D0%B0%D1%80%D1%82%D1%81%D1%8A%D0%B5%D0%B7%D0%B4%D0%B0+%D1%83%D0%BB%2C+%D0%B4%D0%BE%D0%BC+%E2%84%96+5',
                'CITY':'%D0%9E%D0%BC%D1%81%D0%BA',
                'REGION':'%D0%9E%D0%BC%D1%81%D0%BA%D0%B0%D1%8F',
                'PHPSESSID':PHP_SESS,
            },
            'Красноярск': {
                'STORE_ID':'5973',
                'ADDRESS':'60+%D0%BB%D0%B5%D1%82+%D0%9E%D0%B1%D1%80%D0%B0%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F+%D0%A1%D0%A1%D0%A1%D0%A0+%D0%BF%D1%80-%D0%BA%D1%82%2C+%D0%B4%D0%BE%D0%BC+%E2%84%96+30',
                'CITY':'%D0%9A%D1%80%D0%B0%D1%81%D0%BD%D0%BE%D1%8F%D1%80%D1%81%D0%BA',
                'REGION':'%D0%9A%D1%80%D0%B0%D1%81%D0%BD%D0%BE%D1%8F%D1%80%D1%81%D0%BA%D0%B8%D0%B9',
                'PHPSESSID':PHP_SESS,
            },
            'Воронеж ': {
                'STORE_ID':'4724',
                'ADDRESS':'396790%2C+%D0%92%D0%BE%D1%80%D0%BE%D0%BD%D0%B5%D0%B6%D1%81%D0%BA%D0%B0%D1%8F+%D0%BE%D0%B1%D0%BB%2C+%D0%91%D0%BE%D0%B3%D1%83%D1%87%D0%B0%D1%80%D1%81%D0%BA%D0%B8%D0%B9+%D1%80-%D0%BD%2C+%D0%91%D0%BE%D0%B3%D1%83%D1%87%D0%B0%D1%80+%D0%B3%2C+%D0%A2%D0%B5%D0%BD%D0%B8%D1%81%D1%82%D0%B0%D1%8F+%D1%83%D0%BB%2C+%D0%B4%D0%BE%D0%BC+%E2%84%96+25',
                'CITY':'%D0%92%D0%BE%D1%80%D0%BE%D0%BD%D0%B5%D0%B6',
                'REGION':'%D0%92%D0%BE%D1%80%D0%BE%D0%BD%D0%B5%D0%B6%D1%81%D0%BA%D0%B0%D1%8F',
                'PHPSESSID':PHP_SESS,
            },
            'Пермь': {
                'STORE_ID':'4635',
                'ADDRESS':'%D0%9A%D0%B0%D1%80%D0%BF%D0%B8%D0%BD%D1%81%D0%BA%D0%BE%D0%B3%D0%BE+%D1%83%D0%BB%2C+%D0%B4%D0%BE%D0%BC+%E2%84%96+107',
                'CITY':'%D0%9F%D0%B5%D1%80%D0%BC%D1%8C',
                'REGION':'%D0%9F%D0%B5%D1%80%D0%BC%D1%81%D0%BA%D0%B8%D0%B9',
                'PHPSESSID':PHP_SESS,
            },
            'Волгоград': {
                'STORE_ID':'260',
                'ADDRESS':'30-%D0%BB%D0%B5%D1%82%D0%B8%D1%8F+%D0%9F%D0%BE%D0%B1%D0%B5%D0%B4%D1%8B+%D0%B1-%D1%80%2C+%D0%B4%D0%BE%D0%BC+%E2%84%96+16',
                'CITY':'%D0%92%D0%BE%D0%BB%D0%B3%D0%BE%D0%B3%D1%80%D0%B0%D0%B4',
                'REGION':'%D0%92%D0%BE%D0%BB%D0%B3%D0%BE%D0%B3%D1%80%D0%B0%D0%B4%D1%81%D0%BA%D0%B0%D1%8F',
                'PHPSESSID':PHP_SESS,
            },
        }
        self.magasine_date = {'id': 16600, 'name': 'bristol', 'original_logo_url': 'https://bristol.ru/local/templates/bristol/images/logo.svg', 'discount_count': 0}
        self.rub = {}
        self.cookies = self.city_id['Москва']
        self.id_plus = 0

    def start_pars(self):
        try:
            if self.get_update_discounts_discount_company(self.magasine_date['name'])[0]:
                for i in self.city:
                    self.rub = {}
                    if i in self.city_id:
                        self.id_plus = self.city_id_all[i]
                        self.logger_bristol.info(f'bristol Выбран город {i}')
                        self.cookies = self.city_id.get(i)
                        self.logger_bristol.info(f'bristol start parsing rubric {i}')
                        self.rubric()
                        self.logger_bristol.info(f'bristol start parsing tovar {i}')
                        self.pars_id_tovar()
                        self.logger_bristol.info('bristol ADD data discount_city_company')
                        self.add_discount_city_company(i, self.magasine_date['id'] + self.id_plus)
            if self.get_update_discount_filials(self.magasine_date['name']):
                self.magasine_date['discount_count'] = self.get_len_discount(self.magasine_date['id'])
                if not self.get_update_discounts_discount_company(self.magasine_date['name'])[1]:
                    self.add_data_discount_company(self.magasine_date)
                    self.logger_bristol.info(f'bristol {self.magasine_date["name"]} DB discount_company ADD')
        except Exception as e:
            self.logger_bristol.exception(f'Error start_pars bristol')
        self.logger_bristol.info("END PARS BRISTOL")
        print("END BRISTOL")

    #ссылки рубрик
    def rubric(self):
        for i in self.get_soup(self.url).find_all('a', {'class':'bx_catalog_tile_img'}):
            self.rub[i.find('h2').text] = {'src':'https://bristol.ru' + i.get('href')}
            self.logger_bristol.info(f'bristol {i.find("h2").text}')
        self.logger_bristol.info(f'bristol add all category')
        self.add_discount_category(self.rub, self.magasine_date['id'])

    #id всех товаров
    def pars_id_tovar(self):
        for i, items in self.rub.items():
            self.logger_bristol.info(f'bristol start parsing {i}')
            for j in range(self.get_count_page(items['src'])):
                for q in self.get_soup(f'{items["src"]}?PAGEN_1={j}').find_all('a', {'class':'link'}):
                    if i in ['Алкоголь', 'Vape', 'Пиво']:
                        self.pars_data({'original_id':int(q.get('id').split('_')[-2]), 'original_url':f"https://bristol.ru{q.get('href')}", 'adult': True}, rubric1 = i, company_id = self.magasine_date['id'])
                    else:
                        self.pars_data({'original_id': int(q.get('id').split('_')[-2]), 'original_url': f"https://bristol.ru{q.get('href')}", 'adult': False}, rubric1 = i, company_id = self.magasine_date['id'])

    def pars_data(self, data, *args, **kwargs):
        page = self.get_soup(data['original_url'])
        data['thumbnail_url'] = f"https://bristol.ru{page.find('img', {'class':'mainImgItem'}).get('src')}"
        data['product_name'] = page.find('a', {'class', 'leftTitle'}).find('h1').text
        data['price'] = int(float(''.join(page.find('span', {'class':'new'}).text.split(' ')[:-1])) * 100)
        data['description'] = page.find('div', {'class':'bottom wrapInfoMapSection'}).find_all('p')[-1].text.replace('  ', '')
        try:
            data['value_note'] = None
        except: pass
        try:
            data['old_price_note'] = ''.join(page.find('span', {'class':'old'}).text.replace('  ', '').replace('\n', '').split(' ')[:-1]).replace(',', '.').replace('a', '')
            data['promo_type'] = 'PERCENT'
            data['promo_sort_hint'] = round((float(data['old_price_note']) - data['price'] / 100) / (float(data['old_price_note']) / 100))
            data['promo_str'] = f'{data["promo_sort_hint"]}%'
        except: pass
        data['original_company_id'] = self.magasine_date['id'] + self.id_plus
        self.logger_bristol.info(f'bristol ADD DATA {data["product_name"]} - {data["original_id"]} - {data["original_company_id"]}')
        self.add_data_discount(data, *args, **kwargs)

    def get_count_page(self, url):
        try:
            return int(self.get_soup(url).find_all('div', {'class':'btn pag-btn'})[-1].text.replace('\n', ''))
        except:
            return 2

    def get_soup(self, url):
        a = self.requests_get(url, self.headers, cookies = self.cookies)
        return BeautifulSoup(a, 'lxml')