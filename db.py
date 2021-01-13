import pymysql
from pymysql.cursors import DictCursor
from contextlib import closing
from pymysql import Error
from datetime import datetime
import logging.config

class DB:
    def __init__(self):
        logging.config.fileConfig('logs/docs/logging_db.ini', disable_existing_loggers=False)
        self.logger_DB = logging.getLogger(__name__)

        self.host = 'localhost'
        self.user = 'root'
        self.passwd = 'toor'
        self.db_name = 'pars'

        self.get_city = """SELECT * FROM discount_city;"""
        self.get_update_discounts = """SELECT update_discounts FROM discount_company where name=%s"""
        self.get_update_filials_ = """SELECT update_filials FROM discount_company where name=%s"""
        self.get_len_discount_ = """SELECT count(*) FROM discount where original_company_id=%s"""
        self.get_id_category_ = """SELECT id FROM discount_category where name=%s AND company_id=%s;"""

        self.city = self.get_pars_city()

        self.add_data_discount_ = """INSERT discount(created_date, last_modified_date, adult, company_id, description, original_company_id, original_id, original_url, product_name, rubric1, rubric2, rubric3, thumbnail_url, update_elastic) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        self.add_data_discount_category_ = """INSERT discount_category(name, subcategory_of, company_id) VALUES (%s, %s, %s)"""
        self.add_data_discount_city_company_ = """INSERT discount_city_company(created_date, last_modified_date, city_id, update_discounts, company_id, update_filials, discount_count) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        self.add_data_discount_city_company_price_ = """INSERT discount_city_company_price(created_date, last_modified_date, adult, company_id, date_end, date_start, discount_id, removed, old_price_note, original_company_id, price, promo_sort_hint, promo_str, promo_type, update_elastic, value_note) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        self.add_data_discount_company_ = """INSERT discount_company(id, created_date, last_modified_date, discount_count, name, original_logo_url, upd_time, update_discounts, update_filials) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        self.add_data_discount_discount_category_ = """INSERT discount_discount_category(discount_id, category_id) VALUES (%s, %s)"""

        self.update_data_discount_ = """UPDATE discount SET last_modified_date=%s, adult=%s, company_id=%s, description=%s, original_company_id=%s, original_id=%s, original_url=%s, product_name=%s, rubric1=%s, rubric2=%s, rubric3=%s, thumbnail_url=%s, update_elastic=%s where original_id=%s and original_company_id=%s"""
        self.update_data_discount_category_ = """UPDATE discount_category SET name=%s, subcategory_of=%s, company_id=%s where name=%s and company_id=%s;"""
        self.update_data_discount_city_company_ = """UPDATE discount_city_company SET last_modified_date=%s, city_id=%s, update_discounts=%s, company_id=%s, update_filials=%s, discount_count=%s where city_id=%s and company_id=%s;"""
        self.update_data_discount_city_company_price_ = """UPDATE discount_city_company_price SET last_modified_date=%s, adult=%s, company_id=%s, date_end=%s, date_start=%s, discount_id=%s, removed=%s, old_price_note=%s, original_company_id=%s, price=%s, promo_sort_hint=%s, promo_str=%s, promo_type=%s, update_elastic=%s, value_note=%s where discount_id=%s;"""
        self.update_data_discount_company_ = """UPDATE discount_company SET id=%s, last_modified_date=%s, discount_count=%s, name=%s, original_logo_url=%s, upd_time=%s, update_discounts=%s, update_filials=%s where name=%s;"""
        self.update_data_discount_discount_category_ = """UPDATE discount_discount_category SET discount_id=%s, category_id=%s where discount_id=%s and category_id=%s;"""

        self.proof_data_discount_ = """select count(*) from discount where original_id=%s and original_company_id=%s"""
        self.proof_data_discount_category_ = """select count(*) from discount_category where name=%s and company_id=%s;"""
        self.proof_data_discount_city_company_ = """select count(*) from discount_city_company where city_id=%s and company_id=%s;"""
        self.proof_data_discount_city_company_price_ = """select count(*) from discount_city_company_price where discount_id=%s;"""
        self.proof_data_discount_company_ = """select count(*) from discount_company where name=%s;"""
        self.proof_data_discount_discount_category_ = """select count(*) from discount_discount_category where discount_id=%s and category_id=%s;"""

    ####        add_new
    def add_data_discount(self, dat, *args, **kwargs):
        with closing(pymysql.connect(host = self.host, user = self.user, password = self.passwd, db = self.db_name, use_unicode = True, charset='utf8')) as connection:
            with connection.cursor() as cursor:
                create_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                modificate_date = create_date
                adult = dat.get('adult', False)
                company_id = kwargs.get('company_id', None)
                description = dat.get('description', None)
                if description: description = description.replace('  ', '').replace("'", '"')
                original_company_id = dat.get('original_company_id', None)
                original_id = str(dat.get('original_id'))
                original_url = dat.get('original_url')
                product_name = dat.get('product_name')
                if product_name: product_name = product_name.replace("'", '"')
                rubric1 = kwargs.get('rubric1', None)
                rubric2 = kwargs.get('rubric2', None)
                rubric3 = kwargs.get('rubric3', None)
                thumbnail_url = dat.get('thumbnail_url')
                update_elastic = False
                try:
                    if self.proof_data_discount(original_id, original_company_id):
                        cursor.execute(self.add_data_discount_, (create_date, modificate_date, adult, company_id, description, original_company_id, original_id, original_url, product_name, rubric1, rubric2, rubric3, thumbnail_url, update_elastic))
                        self.logger_DB.info(f'ADD_data_discount company_id - {company_id} original_company_id - {original_company_id} original_url - {original_url}')
                    else:
                        cursor.execute(self.update_data_discount_, (modificate_date, adult, company_id, description, original_company_id, original_id, original_url, product_name, rubric1, rubric2, rubric3, thumbnail_url, update_elastic, original_id, original_company_id))
                        self.logger_DB.info(f'UPDATE_data_discount company_id - {company_id} original_company_id - {original_company_id} original_url - {original_url}')
                    connection.commit()
                    for i in [rubric3, rubric2, rubric1]:
                        if i != None:
                            self.add_discount_discount_category(i, original_id, company_id, original_company_id)
                            break
                    self.add_discount_city_company_price(dat, *args, **kwargs)
                except Exception as e:
                    self.logger_DB.exception(f'Error add_data_discount {dat}')

    def add_data_discount_company(self, dat, *args, **kwargs):
        with closing(pymysql.connect(host = self.host, user = self.user, password = self.passwd, db = self.db_name, use_unicode=True, charset='utf8')) as connection:
            with connection.cursor() as cursor:
                id_ = dat.get('id', 16399)
                create_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                last_modified_date = create_date
                name = dat.get('name', 'xxx')
                original_logo_url = dat.get('original_logo_url', '')
                upd_time = create_date
                update_discounts = True
                update_filials = True
                dicount_count = self.get_all_len_discount(id_)
                try:
                    if self.proof_data_discount_company(name):
                        cursor.execute(self.add_data_discount_company_, (id_, create_date, last_modified_date, dicount_count, name, original_logo_url, upd_time, update_discounts, update_filials))
                        self.logger_DB.info(f'ADD_data_discount_company id_ - {id_} name - {name}')
                    else:
                        cursor.execute(self.update_data_discount_company_, (id_, last_modified_date, dicount_count, name, original_logo_url, upd_time, update_discounts, update_filials, name))
                        self.logger_DB.info(f'UPDATE_data_discount_company id_ - {id_} name - {name}')
                except Exception as e:
                    self.logger_DB.exception(f'Error add_data_discount_company {dat}')
                connection.commit()

    def add_discount_category(self, rub, com_id, *args, **kwargs):
        with closing(pymysql.connect(host = self.host, user = self.user, password = self.passwd, db = self.db_name, use_unicode=True, charset='utf8')) as connection:
            with connection.cursor() as cursor:
                for i, items in rub.items():
                    name = i
                    if kwargs.get('sub_of', -1) != -1: subcategory_of = self.get_id_category(kwargs.get('sub_of'), com_id)
                    else: subcategory_of = None
                    company_id = com_id
                    try:
                        if self.proof_data_discount_category(name, company_id):
                            cursor.execute(self.add_data_discount_category_, (name, subcategory_of, company_id))
                            self.logger_DB.info(f'ADD_discount_category com_id - {com_id} name - {name}')
                        else:
                            cursor.execute(self.update_data_discount_category_, (name, subcategory_of, company_id, name, company_id))
                            self.logger_DB.info(f'UPDATE_discount_category com_id - {com_id} name - {name}')
                        connection.commit()
                    except Exception as e:
                        self.logger_DB.exception(f'Error add_discount_category {rub} - {company_id}')

                    if 'src' not in items:
                        self.add_discount_category(items, com_id, sub_of = i)

    def add_discount_city_company(self, city, id_, *args, **kwargs):
        with closing(pymysql.connect(host = self.host, user = self.user, password = self.passwd, db = self.db_name, use_unicode=True, charset='utf8')) as connection:
            with connection.cursor() as cursor:
                create_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                last_modified_date = create_date
                city_id = self.get_id_city(city)
                update_discounts = True
                company_id = id_
                update_filials = True
                discount_count = self.get_len_discount(id_)
                try:
                    if self.proof_data_discount_city_company(city_id, company_id):
                        cursor.execute(self.add_data_discount_city_company_, (create_date, last_modified_date, city_id, update_discounts, company_id, update_filials, discount_count))
                        self.logger_DB.info(f'ADD_discount_city_company city_id - {city_id} company_id - {company_id} disc_count - {discount_count}')
                    else:
                        cursor.execute(self.update_data_discount_city_company_, (last_modified_date, city_id, update_discounts, company_id, update_discounts, discount_count, city_id, company_id))
                        self.logger_DB.info(f'UPDATE_discount_city_company city_id - {city_id} company_id - {company_id} disc_count - {discount_count}')
                    connection.commit()
                except Exception as e:
                    self.logger_DB.exception(f'Error add_discount_city_company {city} - {id_}')

    def add_discount_discount_category(self, name_rub, or_id, com_id, original_company_id, *args, **kwargs):
        with closing(pymysql.connect(host = self.host, user = self.user, password = self.passwd, db = self.db_name, use_unicode=True, charset='utf8')) as connection:
            with connection.cursor() as cursor:
                discount_id = self.get_id_discount(original_company_id, or_id)
                category_id = self.get_id_category(name_rub, com_id)
                try:
                    if self.proof_data_discount_discount_category(discount_id, category_id):
                        cursor.execute(self.add_data_discount_discount_category_, (discount_id, category_id))
                        self.logger_DB.info(f'ADD_discount_discount_category category_id - {category_id} discount_id - {discount_id}')
                    else:
                        cursor.execute(self.update_data_discount_discount_category_, (discount_id, category_id, discount_id, category_id))
                        self.logger_DB.info(f'UPDATE_discount_discount_category category_id - {category_id} discount_id - {discount_id}')
                    connection.commit()
                except Exception as e:
                    self.logger_DB.exception(f'Error add_discount_discount_category {name_rub} - {or_id} - {com_id} - {original_company_id}')

    def add_discount_city_company_price(self, data, *args, **kwargs):
        with closing(pymysql.connect(host=self.host, user=self.user, password=self.passwd, db=self.db_name, use_unicode=True, charset='utf8')) as connection:
            with connection.cursor() as cursor:
                create_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')#
                last_modified_date = create_date#
                adult = data.get('adult', False)#
                company_id = kwargs.get('company_id', 16399)#
                date_end = data.get('date_end', None)
                date_start = data.get('date_start', None)
                discount_id = self.get_id_discount(data.get('original_company_id', None), data.get('original_id', None))
                removed = False #
                old_price_note = data.get('old_price_note', None)#
                original_company_id = data.get('original_company_id', None)#
                price = data.get('price', None)#
                promo_sort_hint = data.get('promo_sort_hint', None)#
                promo_str = data.get('promo_str', None)#
                promo_type = data.get('promo_type', None)#
                update_elastic = False #
                value_note = data.get('value_note', None)#
                try:
                    if self.proof_data_discount_city_company_price(discount_id):
                        cursor.execute(self.add_data_discount_city_company_price_ ,(create_date, last_modified_date, adult, company_id, date_end, date_start, discount_id, removed, old_price_note, original_company_id, price, promo_sort_hint, promo_str, promo_type, update_elastic, value_note))
                        self.logger_DB.info(f'ADD_discount_city_company_price discount_id - {discount_id}')
                    else:
                        cursor.execute(self.update_data_discount_city_company_price_, (last_modified_date, adult, company_id, date_end, date_start, discount_id, removed, old_price_note, original_company_id, price, promo_sort_hint, promo_str, promo_type, update_elastic, value_note, discount_id))
                        self.logger_DB.info(f'UPDATE_discount_city_company_price discount_id - {discount_id}')
                    connection.commit()
                except Exception as e:
                    self.logger_DB.exception(f'Error add_discount_city_company_price  {data}')

    ####        get_data
    def get_id_discount(self, id_, or_id):
        with closing(pymysql.connect(host = self.host, user = self.user, password = self.passwd, db = self.db_name, charset='utf8mb4', cursorclass=DictCursor)) as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute("""select id from discount where original_company_id=%s and original_id=%s""", (id_, or_id))
                    return cursor.fetchall()[0].get('id')
                except:
                    self.logger_DB.info(f'NOT FOUND get_id_discount {id_} - {or_id}')

    def get_all_len_discount(self, id_):
        with closing(pymysql.connect(host = self.host,user = self.user,password = self.passwd, db = self.db_name, charset='utf8mb4', cursorclass=DictCursor)) as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute("""select count(*) from discount where company_id=%s""", (id_, ))
                    return cursor.fetchall()[0]['count(*)']
                except:
                    self.logger_DB.info(f'NOT FOUND get_all_len_discount {id_}')

    def get_pars_city(self):
        with closing(pymysql.connect(host = self.host,user = self.user,password = self.passwd, db = self.db_name, charset='utf8mb4', cursorclass=DictCursor)) as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(self.get_city)
                    return [i['name'] for i in cursor.fetchall() if i['update_discounts'] == b'\x01']
                except:
                    self.logger_DB.info(f'NOT FOUND get_pars_city')

    def get_len_discount(self, id_):
        with closing(pymysql.connect(host = self.host, user = self.user, password = self.passwd, db = self.db_name, use_unicode=True, charset='utf8')) as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(self.get_len_discount_ %id_)
                    return cursor.fetchall()[0][0]
                except:
                    self.logger_DB.info(f'NOT FOUND get_len_discount {id_}')
                    return 0

    def get_update_discounts_discount_company(self, name, *args, **kwargs):
        with closing(pymysql.connect(host = self.host, user = self.user, password = self.passwd, db = self.db_name, use_unicode=True, charset='utf8')) as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(self.get_update_discounts %name)
                    if cursor.fetchall()[0] == b'0': return False, True
                    else: return True, True
                except:
                    self.logger_DB.info(f'NOT FOUND get_update_discounts_discount_company {name}')
                    return True, False #второе значение для определения существует ли сейчас данное поле, чтобы выбрать создавать его или обнолять

    def get_update_discount_filials(self, name):
        with closing(pymysql.connect(host = self.host, user = self.user, password = self.passwd, db = self.db_name, use_unicode=True, charset='utf8')) as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(self.get_update_filials_ ,(name,))
                    if cursor.fetchall()[0] == b'0': return False
                    else: return True
                except:
                    self.logger_DB.info(f'NOT FOUND get_update_discount_filials {name}')
                    return True

    def get_id_category(self, name, id_):
        with closing(pymysql.connect(host = self.host, user = self.user, password = self.passwd, db = self.db_name, use_unicode=True, charset='utf8')) as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(self.get_id_category_, (name, id_))
                    return cursor.fetchall()[0][0]
                except:
                    self.logger_DB.info(f'NOT FOUND get_id_category {name} - {id_}')
                    return 0

    def get_id_city(self, name):
        with closing(pymysql.connect(host = self.host, user = self.user, password = self.passwd, db = self.db_name, use_unicode=True, charset='utf8')) as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute("""select original_id from discount_city where name=%s""" ,(name, ))
                    return cursor.fetchall()[0][0]
                except:
                    self.logger_DB.info(f'NOT FOUND get_id_category {name}')
                    return 16399

    ####        proof_data
    def proof_data_discount(self, id_, q):
        with closing(pymysql.connect(host = self.host, user = self.user, password = self.passwd, db = self.db_name, charset='utf8mb4', cursorclass=DictCursor)) as connection:
            with connection.cursor() as cursor:
                cursor.execute(self.proof_data_discount_, (id_, q))
                if cursor.fetchall()[0]['count(*)'] == 1: return False
                else: return True

    def proof_data_discount_category(self, name, company_id):
        with closing(pymysql.connect(host = self.host, user = self.user, password = self.passwd, db = self.db_name, charset='utf8mb4', cursorclass=DictCursor)) as connection:
            with connection.cursor() as cursor:
                cursor.execute(self.proof_data_discount_category_, (name, company_id))
                if cursor.fetchall()[0]['count(*)'] == 0: return True
                else: return False

    def proof_data_discount_city_company(self, city_id, company_id):
        with closing(pymysql.connect(host = self.host, user = self.user, password = self.passwd, db = self.db_name, charset='utf8mb4', cursorclass=DictCursor)) as connection:
            with connection.cursor() as cursor:
                cursor.execute(self.proof_data_discount_city_company_, (city_id, company_id))
                if cursor.fetchall()[0]['count(*)'] == 0: return True
                else: return False

    def proof_data_discount_city_company_price(self, discount_id):
        with closing(pymysql.connect(host = self.host, user = self.user, password = self.passwd, db = self.db_name, charset='utf8mb4', cursorclass=DictCursor)) as connection:
            with connection.cursor() as cursor:
                cursor.execute(self.proof_data_discount_city_company_price_, (discount_id, ))
                if cursor.fetchall()[0]['count(*)'] == 0: return True
                else: return False

    def proof_data_discount_company(self, name):
        with closing(pymysql.connect(host = self.host, user = self.user, password = self.passwd, db = self.db_name, charset='utf8mb4', cursorclass=DictCursor)) as connection:
            with connection.cursor() as cursor:
                cursor.execute(self.proof_data_discount_company_, (name))
                if cursor.fetchall()[0]['count(*)'] == 0: return True
                else: return False

    def proof_data_discount_discount_category(self, discount_id, category_id):
        with closing(pymysql.connect(host = self.host, user = self.user, password = self.passwd, db = self.db_name, charset='utf8mb4', cursorclass=DictCursor)) as connection:
            with connection.cursor() as cursor:
                cursor.execute(self.proof_data_discount_discount_category_, (discount_id, category_id))
                if cursor.fetchall()[0]['count(*)'] == 0: return True
                else: return False

    ####    tests
    def clear_all(self):
        with closing(pymysql.connect(host = self.host, user = self.user, password = self.passwd, db = self.db_name, charset='utf8mb4', cursorclass=DictCursor)) as connection:
            with connection.cursor() as cursor:
                for i in ['discount', 'discount_category', 'discount_city_company', 'discount_discount_category', 'discount_company', 'discount_city_company_price']:
                    cursor.execute(f'TRUNCATE TABLE  {i}')
                    print(f'clear table {i}')
                    connection.commit()

    def test(self):
        with closing(pymysql.connect(host = self.host, user = self.user, password = self.passwd, db = self.db_name, charset='utf8mb4', cursorclass=DictCursor)) as connection:
            with connection.cursor() as cursor:
                for i in ['discount', 'discount_category', 'discount_city_company', 'discount_discount_category', 'discount_company', 'discount_city_company_price']:
                    cursor.execute(f'select * from {i}')
                    print(f'TABLE {i}')
                    for j in cursor.fetchall():
                        print(j)