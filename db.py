import pymysql
from pymysql.cursors import DictCursor
from contextlib import closing
from pymysql import Error
from datetime import datetime

class DB:
    def __init__(self):
        self.get_city = 'SELECT * FROM discount_city;'

        self.city = self.get_pars_city()

        self.add_data_discount = 'INSERT discount(created_date, last_modified_date, adult, company_id, description, original_company_id, original_id, original_url, product_name, removed, rubric1, rubric2, rubric3, thumbnail_url, update_elastic) VALUES (%s)'
        self.add_data_discount_category = 'INSERT discount_category(name, subcategory_of, company_id) VALUES ()'
        self.add_data_discount_city_company = 'INSERT discount_city_company(created_date, last_modified_date, city_id, update_discounts, company_id, update_filials, discount_count) VALUES ()'
        self.add_data_discount_city_company_price = 'INSERT discount_city_company_price(created_date, last_modified_date, abult, company_id, date_end, date_start, discount_id, old_price_note, original_company_id, price, promo_sort_hint, promo_str, promo_type, update_elastic, value_note) VALUES ()'
        self.add_data_discount_company = 'INSERT discount_company(created_date, last_modified_date, city_id, discount_count, name, original_city_id, original_logo_url, upd_time, update_discounts, update_filials) VALUES ()'
        self.add_data_discount_discount_category = 'INSERT discount_discount_category(discount_id, category_id) VALUES ()'


    def add_data(self, dat, *args, **kwargs):
        with closing(pymysql.connect(host='localhost',user='root',password='toor', db='pars', charset='utf8mb4', cursorclass=DictCursor)) as connection:
            with connection.cursor() as cursor:
                create_date = datetime.now()


    def get_pars_city(self):
        with closing(pymysql.connect(host='localhost',user='root',password='toor', db='pars', charset='utf8mb4', cursorclass=DictCursor)) as connection:
            with connection.cursor() as cursor:
                cursor.execute(self.get_city)
                return [i['name'] for i in cursor.fetchall() if i['update_discounts'] == b'\x01']