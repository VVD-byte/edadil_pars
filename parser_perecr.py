from parser import pars
import json
import logging.config
from bs4 import BeautifulSoup

class pars_perecr(pars):
    def __init__(self):
        super().__init__()
        logging.config.fileConfig('logs/docs/logging_bristol.ini', disable_existing_loggers=False)
        self.logger_perecr = logging.getLogger(__name__)
        self.url = 'https://www.vprok.ru/catalog'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        }
        self.rub = {}
        self.city_id = {
            'Москва': '1',
            'Санкт-Петербург': '2',
            'Екатеринбург': '29',
            'Нижний Новгород': '3',
            'Челябинск': '38',
            'Самара': '27',
            'Ростов-на-Дону': '25',
            'Воронеж ': '10',
            'Пермь': '20',
            'Волгоград': '46',
        }
        self.magasine_date = {'id': 16800, 'name': 'perecrestok', 'original_logo_url': '', 'discount_count': 0}
        self.id_plus = 0
        self.cookies = {}

    def start_pars(self):
        try:
            if self.get_update_discounts_discount_company(self.magasine_date['name'])[0]:
                self.magasine_date['original_logo_url'] = 'https://www.vprok.ru/' + self.get_soup(self.url).find('img', {'class':'xfnew-header__logo-image xfnew-header__logo-image--new-year'}).get('src')
                for i in self.city:
                    self.rub = {}
                    if i in self.city_id:
                        self.id_plus = self.city_id_all[i]
                        self.logger_perecr.info(f'perecrestok Выбран город {i}')
                        self.cookies = {'region':self.city_id.get(i)}
                        self.logger_perecr.info(f'perecrestok start parsing rubric {i}')
                        self.rubric()
                        self.logger_perecr.info(f'perecrestok start parsing tovar {i}')
                        self.pars_id_tovar(self.rub)
                        self.add_discount_city_company(i, self.magasine_date['id'] + self.id_plus)
            if self.get_update_discount_filials(self.magasine_date['name']):
                self.magasine_date['discount_count'] = self.get_len_discount(self.magasine_date['id'])
                if not self.get_update_discounts_discount_company(self.magasine_date['name'])[1]:
                    self.add_data_discount_company(self.magasine_date)
                    self.logger_perecr.info(f'perecrestok {self.magasine_date["name"]} DB discount_company ADD')
        except Exception as e:
            self.logger_perecr.exception(f'Error start_pars perecrest')

    def rubric(self):
        for id_, i in enumerate(self.get_soup(self.url).find_all('a', {'class':'xf-catalog-categories__link'})[:24]):
            self.rub[i.text.replace('  ', '').replace('\n', '')] = {}
            try:
                for j in self.get_soup('https://www.vprok.ru' + i.get('href')).find_all('a', {'class':'xf-filter__item-label xf-ripple js-xf-ripple xf-ripple_gray'}):
                    self.rub[i.text.replace('  ', '').replace('\n', '')][j.text.replace('  ', '').replace('\n', '')] = {}
                    if 'Разделы' in self.get_soup('https://www.vprok.ru' + j.get('href')).find('span', {'class':'xf-filter__header-text js-shave-container'}).text:
                        try:
                            for q in self.get_soup('https://www.vprok.ru' + j.get('href')).find_all('a', {'class':'xf-filter__item-label xf-ripple js-xf-ripple xf-ripple_gray'}):
                                self.rub[i.text.replace('  ', '').replace('\n', '')][j.text.replace('  ', '').replace('\n', '')][q.text.replace('  ', '').replace('\n', '')] = {}
                                self.rub[i.text.replace('  ', '').replace('\n', '')][j.text.replace('  ', '').replace('\n', '')][q.text.replace('  ', '').replace('\n', '')]['src'] = 'https://www.vprok.ru' + q.get('href')
                        except:
                            self.rub[i.text.replace('  ', '').replace('\n', '')][j.text.replace('  ', '').replace('\n', '')]['src'] = 'https://www.vprok.ru' + j.get('href')
                    else:
                        self.rub[i.text.replace('  ', '').replace('\n', '')][j.text.replace('  ', '').replace('\n', '')]['src'] = 'https://www.vprok.ru' + j.get('href')
            except:
                self.rub[i.text.replace('  ', '').replace('\n', '')]['src'] = 'https://www.vprok.ru' + i.get('href')
        self.add_discount_category(self.rub, self.magasine_date['id'])

    def get_soup(self, url):
        a = self.requests_get(url, self.headers, cookies = self.cookies)
        return BeautifulSoup(a, 'lxml')

    def get_soup_(self, url):
        a = self.requests_get_(url, self.headers, cookies = self.cookies)
        return BeautifulSoup(a[0], 'lxml'), a[1]

    def pars_id_tovar(self, dats, *args, **kwargs):
        for i, items in dats.items():
            if 'src' in items:
                self.get_pars_page(items, i, *args, **kwargs)
            else:
                self.pars_id_tovar(items, i, *args, **kwargs)

    def get_pars_page(self, dat, *args, **kwargs):
        if len(args) == 3: kwargs = {'rubric1':args[::-1][0], 'rubric2':args[::-1][1], 'rubric3':args[::-1][2]}
        elif len(args) == 2: kwargs = {'rubric1': args[::-1][0], 'rubric2': args[::-1][1]}
        else: kwargs = {'rubric1': args[::-1][0]}
        self.get_all_data(self.get_soup(dat['src']), *args, **kwargs)
        for i in range(2, 100):
            req = self.get_soup_(dat['src'] + f'?page={i}')
            if req[1] != dat['src']:
                self.get_all_data(req[0], *args, **kwargs)
            else:
                break

    def get_all_data(self, page, *args, **kwargs):
        for i in page.find_all('li', {'class':'js-catalog-product _additionals xf-catalog__item'}):
            if 'отсутств' not in i.text:
                data = {}
                data['original_url'] = 'https://www.vprok.ru' + i.find('a', {'class':'xf-product-picture__link js-product__image'}).get('href')
                data['original_id'] = i.find('div').get('data-id')
                if page.find('div', {'class':'xf-empty-cart-popup _age'}): data['adult'] = True
                else: data['adult'] = False
                data['thumbnail_url'] = i.find('img', {'class':'js-lazy tns-lazy-img xf-product-picture__img js-product-picture__img-single'}).get('data-src')
                data['product_name'] = i.find('a', {'class':'xf-product-title__link'}).get('title').replace('  ', '').replace('\n', '')
                data['price'] = int(float(''.join(page.find('span', {'class': 'xf-hidden'}).text)) * 100)
                data['description'] = None
                try:
                    data['value_note'] = '₽/' + i.find('span', {'class':'xf-price__unit'}).text.split('/')[1]
                except:
                    data['value_note'] = None
                try:
                    data['old_price_note'] = i.find('div', {'class':'xf-price xf-product-cost__prev js-product__old-cost'}).get('data-cost')
                    data['promo_type'] = 'PERCENT'
                    data['promo_sort_hint'] = int(i.find('p', {'class':'js-calculated-discount'}).text)
                    data['promo_str'] = f'{data["promo_sort_hint"]}%'
                except:
                    pass
                data['original_company_id'] = self.magasine_date['id'] + self.id_plus
                self.add_data_discount(data, company_id = self.magasine_date['id'], *args, **kwargs)