import pymysql
from pymysql.cursors import DictCursor
from contextlib import closing
from pymysql import Error
from datetime import datetime
from time import sleep

class DB:
    def __init__(self):
        self.get_city = 'SELECT * FROM discount_city;'
        self.get_update_discounts = 'SELECT update_discounts FROM discount_company where name="%s"'
        self.get_len_discount_ = 'SELECT count(*) FROM discount where company_id=%s'
        self.get_id_category_ = 'SELECT id FROM discount_category where name="%s" AND company_id=%s;'

        self.city = self.get_pars_city()

        self.add_data_discount_ = "INSERT discount (created_date, last_modified_date, adult, company_id, description, original_company_id, original_id, original_url, product_name, rubric1, rubric2, rubric3, thumbnail_url, update_elastic) VALUES('%s', '%s', %s, %s, '%s', %s, %s, '%s', '%s', '%s', '%s', '%s', '%s', %s);"
        self.add_data_discount_category_ = "INSERT discount_category(name, subcategory_of, company_id) VALUES ('%s', %s, %s)"
        self.add_data_discount_city_company_ = 'INSERT discount_city_company(created_date, last_modified_date, city_id, update_discounts, company_id, update_filials, discount_count) VALUES ()'
        self.add_data_discount_city_company_price = 'INSERT discount_city_company_price(created_date, last_modified_date, abult, company_id, date_end, date_start, discount_id, old_price_note, original_company_id, price, promo_sort_hint, promo_str, promo_type, update_elastic, value_note) VALUES ()'
        self.add_data_discount_company_ = "INSERT discount_company(id, created_date, last_modified_date, discount_count, name, original_logo_url, upd_time, update_discounts, update_filials) VALUES (%s, '%s', '%s', %s, '%s', '%s', '%s', %s, %s)"
        self.add_data_discount_discount_category = 'INSERT discount_discount_category(discount_id, category_id) VALUES ()'

    ####        add_new
    def add_data_discount(self, dat, *args, **kwargs):
        with closing(pymysql.connect(host='localhost',user='root',password='toor', db='pars', use_unicode = True, charset='utf8')) as connection:
            with connection.cursor() as cursor:
                create_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                modificate_date = create_date
                adult = dat.get('adult', b'0')
                company_id = kwargs.get('company_id', 16399)
                description = dat.get('description', '').replace('  ', '').replace("'", '"')
                original_company_id = company_id
                original_id = dat.get('original_id')
                original_url = dat.get('original_url')
                product_name = dat.get('product_name').replace("'", '"')
                rubric1 = kwargs.get('rubric1', 'null')
                rubric2 = kwargs.get('rubric2', 'null')
                rubric3 = kwargs.get('rubric3', 'null')
                thumbnail_url = dat.get('thumbnail_url')
                update_elastic = b'0'
                try:
                    cursor.execute(self.add_data_discount_ %(create_date, modificate_date, adult, company_id, description, original_company_id, original_id, original_url, product_name, rubric1, rubric2, rubric3, thumbnail_url, update_elastic))
                except Error as e:
                    print(self.add_data_discount_ %(create_date, modificate_date, adult, company_id, description, original_company_id, original_id, original_url, product_name, rubric1, rubric2, rubric3, thumbnail_url, update_elastic))
                    raise e
                connection.commit()

    def add_data_discount_company(self, dat, *args, **kwargs):
        with closing(pymysql.connect(host='localhost', user='root', password='toor', db='pars', use_unicode=True, charset='utf8')) as connection:
            with connection.cursor() as cursor:
                id = dat.get('id', 16399)
                create_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                last_modified_date = create_date
                name = dat.get('name', 'xxx')
                original_logo_url = dat.get('original_logo_url', '')
                upd_time = create_date
                update_discounts = b'1'
                update_filials = b'1'
                dicount_count = dat.get('discount_count', 0)
                try:
                    cursor.execute(self.add_data_discount_company_ %(id, create_date, last_modified_date, dicount_count, name, original_logo_url, upd_time, update_discounts, update_filials))
                except Error as e:
                    print(self.add_data_discount_company_ %(id, create_date, last_modified_date, dicount_count, name, original_logo_url, upd_time, update_discounts, update_filials))
                    raise e
                connection.commit()

    def add_discount_category(self, rub, com_id, *args, **kwargs):
        with closing(pymysql.connect(host='localhost', user='root', password='toor', db='pars', use_unicode=True, charset='utf8')) as connection:
            with connection.cursor() as cursor:
                for i, items in rub.items():
                    name = i
                    if kwargs.get('sub_of', -1) != -1: subcategory_of = self.get_id_category(kwargs.get('sub_of'), com_id)
                    else: subcategory_of = 'null'
                    company_id = com_id
                    cursor.execute(self.add_data_discount_category_ %(name, subcategory_of, company_id))
                    connection.commit()
                    sleep(1)
                    if 'src' not in items:
                        self.add_discount_category(items, com_id, sub_of = i)

    def add_discount_city_company(self, city_id, original_city_id):
        with closing(pymysql.connect(host='localhost', user='root', password='toor', db='pars', use_unicode=True, charset='utf8')) as connection:
            with connection.cursor() as cursor:
                create_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                last_modified_date = create_date

    ####        update_data

    ####        get_data
    def get_pars_city(self):
        with closing(pymysql.connect(host='localhost',user='root',password='toor', db='pars', charset='utf8mb4', cursorclass=DictCursor)) as connection:
            with connection.cursor() as cursor:
                cursor.execute(self.get_city)
                return [i['name'] for i in cursor.fetchall() if i['update_discounts'] == b'\x01']

    def get_len_discount(self, id):
        with closing(pymysql.connect(host='localhost', user='root', password='toor', db='pars', use_unicode=True, charset='utf8')) as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(self.get_len_discount_ %id)
                    return cursor.fetchall()[0][0]
                except: return 0

    def get_update_discounts_discount_company(self, name, *args, **kwargs):
        with closing(pymysql.connect(host='localhost', user='root', password='toor', db='pars', use_unicode=True, charset='utf8')) as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(self.get_update_discounts %name)
                    if cursor.fetchall()[0] == b'0': return False, True
                    else: return True, True
                except: return True, False #второе значение для определения существует ли сейчас данное поле, чтобы выбрать создавать его или обнолять

    def get_id_category(self, name, id_):
        with closing(pymysql.connect(host='localhost', user='root', password='toor', db='pars', use_unicode=True, charset='utf8')) as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(self.get_id_category_ %(name, id_))
                    return cursor.fetchall()[0][0]
                except:
                    return 0

    ####        manipulate_data
    def clear_all_discount(self):
        with closing(pymysql.connect(host='localhost',user='root',password='toor', db='pars', charset='utf8mb4', cursorclass=DictCursor)) as connection:
            with connection.cursor() as cursor:
                cursor.execute(f'TRUNCATE TABLE discount')
                connection.commit()

    def clear_all_category(self):
        with closing(pymysql.connect(host='localhost',user='root',password='toor', db='pars', charset='utf8mb4', cursorclass=DictCursor)) as connection:
            with connection.cursor() as cursor:
                cursor.execute(f'TRUNCATE TABLE discount_category')
                connection.commit()