import json
from parser import pars
import logging.config
from bs4 import BeautifulSoup
from requests import ConnectionError

class pars_yarche(pars):
    def __init__(self):
        super().__init__()
        logging.config.fileConfig('logs/docs/logging_yarche.ini', disable_existing_loggers=False)
        self.logger_yarche = logging.getLogger(__name__)

        self.city_id = {
            'Москва': '16375',
            'Новосибирск': '16915',
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        }
        self.url = 'https://yarcheplus.ru/category'
        self.city_id = {
                'Москва':'9b7a0df48d25b5c2e76a02c54ccbfbc8ced90480-7a0d48babd20b824d5eda9523f71c67c2d639b43',
                'Новосибирск':'cdde72ec4b8afa454c65721f83d0544ac72e488a-283456e23a26a069cbb0537782e7ad18ca747890',
                } ## cookies token привязан к городу
        self.rub = {}
        self.cookies = {}
        self.id_plus = 0
        self.magasine_date = {'id': 16500, 'name': 'fix_price', 'original_logo_url': 'https://yarcheplus.ru/static/images/build/logo_new_year-3df8111aeb8588581d57287795917fb8.svg', 'discount_count': 0}

    def start_pars(self):
        try:
            if self.get_update_discounts_discount_company(self.magasine_date['name'])[0]:
                for i in self.city:
                    self.rub = {}
                    if i in self.city_id:
                        self.id_plus = self.city_id_all[i]
                        self.logger_yarche.info(f'yarche Выбран город {i}')
                        self.cookies = {'token':self.city_id[i]}
                        self.logger_yarche.info(f'yarche start parsing rubric {i}')
                        self.rubric()
                        self.logger_yarche.info(f'yarche start parsing tovar {i}')
                        self.pars_id_tovar()
                        self.add_discount_city_company(i, self.magasine_date['id'] + self.id_plus)
            if self.get_update_discount_filials(self.magasine_date['name']):
                self.magasine_date['discount_count'] = self.get_len_discount(self.magasine_date['id'])
                if not self.get_update_discounts_discount_company(self.magasine_date['name'])[1]:
                    self.add_data_discount_company(self.magasine_date)
                    self.logger_yarche.info(f'yarche {self.magasine_date["name"]} DB discount_company ADD')
        except Exception as e:
            self.logger_yarche.exception(f'Error start_pars yarche')
        self.logger_yarche.info("END PARS YARCHE")
        print("END YARCHE")

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
            self.logger_yarche.info(f'RUBRIC ALL COLLECT yarche')
        except Exception as e:
            self.logger_yarche.exception(f'Error rubric yarche')
        try:
            self.add_discount_category(self.rub, self.magasine_date['id'])
        except Exception as e:
            self.logger_yarche.exception(f'Error add category rubric yarche')

    def pars_id_tovar(self):
        try:
            for i, items in self.rub.items():
                if 'src' in items:
                    self.logger_yarche.info(f'yarche start parsing_ {i}')
                    self.get_page_tovar(items)
                    self.get_tovar(items, rubric1 = i, company_id = self.magasine_date['id'])
                    self.rub[i] = {}
                else:
                    for j, item in items.items():
                        if 'src' in item:
                            self.logger_yarche.info(f'yarche start parsing {j}')
                            self.get_page_tovar(item)
                            self.get_tovar(item, rubric1 = i, rubric2 = j, company_id = self.magasine_date['id'])
                            self.rub[i][j] = {}
        except Exception as e:
            self.logger_yarche.exception(f'Error pars_id_tovar yarche')

    def get_page_tovar(self, data):
        try:
            for i in range(1, self.get_len_page(data['src'])):
                try:
                    for j in self.get_soup(data['src'] + f'?page={i}').find_all('div', {'class':'c3s8K6a5X'}):
                        try:
                            name = j.find('a', {'class':'f2mGXj5-x'}).get('href').split('/')[-1]
                            data[name] = {}
                            data[name]['original_id'] = name
                            data[name]['original_url'] = 'https://yarcheplus.ru' + j.find('a', {'class':'f2mGXj5-x'}).get('href')
                            data[name]['thumbnail_url'] = j.find('img', {'class':'k2mGXj5-x'}).get('src')
                            data[name]['product_name'] = j.find('a', {'class':'f2mGXj5-x'}).text
                            data[name]['adult'] = False
                            data[name]['price'] = int(float(j.find('div', {'class':'a34tOzx2Q'}).text.replace(' ', '').replace('₽', '').replace(',', '.')) * 100)
                            try: data[name]['value_note'] = j.find('div', {'class':'a34tOzx2Q'}).text + ' ' + j.find('div', {'class':'b34tOzx2Q'}).text
                            except: pass
                            try:
                                data[name]['old_price_note'] = ''.join(j.find('div', {'class':'c34tOzx2Q'}).text.split(' ')[:-1]).replace(',', '.')
                                data[name]['promo_type'] = 'PERCENT'
                                data[name]['promo_sort_hint'] = round((float(data[name]['old_price_note']) - data[name]['price']/100)/(float(data[name]['old_price_note'])/100))
                                data[name]['promo_str'] = f'{data[name]["promo_sort_hint"]}%'
                            except: pass
                            data[name]['original_company_id'] = self.magasine_date['id'] + self.id_plus
                        except Exception as e:
                            self.logger_yarche.exception(f'Error get_page_tovar page-{i, j} url-{data["src"]} yarche')
                except Exception as e:
                    self.logger_yarche.exception(f'Error get_page_tovar page-{i} url-{data["src"]} yarche')
        except Exception as e:
            self.logger_yarche.exception(f'Error get_page_tovar all yarche')

    def get_len_page(self, url):
        try:
            return int(self.get_soup(url).find_all('a', {'class':'b18ybbMcB'})[-2])
        except:
            return 2

    def get_soup(self, url):
        try:
            a = self.requests_get(url, self.headers, cookies = self.cookies)
            return BeautifulSoup(a, 'lxml')
        except Exception as e:
            self.logger_yarche.exception(f'Error get_soup yarche')

    def get_tovar(self, data, *args, **kwargs):
        try:
            for i, items in data.items():
                if i != 'src':
                    dat = self.get_soup(items.get('original_url', ''))
                    items['description'] = dat.find('div', {'class':'fa3QZxpOf a2Q0qeMRL d2Q0qeMRL'}).text
                    self.logger_yarche.info(f'yarche ADD DATA {items["product_name"]} - {items["original_id"]} - {items["original_company_id"]}')
                    self.add_data_discount(items, *args, **kwargs)
        except Exception as e:
            self.logger_yarche.exception(f'Error get_tovar yarche')

    @staticmethod
    def clear_soup_text(text):
        return text.text.replace('  ', '').replace('\n', '')