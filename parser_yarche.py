import json
from parser import pars
from db import DB

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
        self.headers_yarche = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'token': '60da36a4209f226ee22a9506b5677c26bbad7ce8-7472824d32d3c907fc3eecca290c5015cb905448',
            'Content-Type': 'application/json',
        }
        self.url = 'http://api.magonline.ru/api/graphql'
        self.start, self.end = 80, 300

    def start_pars(self):
        for i in range(self.start, self.end):
            self.data_yarce['variables']['categoryId'] = i
            a = self.requests_post(_url = self.url, head = self.headers_yarche, dat = json.dumps(self.data_yarce))
            try:
                if a['data']['products']['page']['total'] != 0:
                    self.DB(a)
                if a['data']['products']['page']['total'] > 100:
                    self.get_all_page(a['data']['products']['page']['total'])
            except:
                pass

    def get_all_page(self, len_data):
        for i in range(2, len_data//100 + 2):
            self.data_yarce['variables']['pagination']['page'] = i
            a = self.requests_post(_url = self.url, head = self.headers_yarche, dat = json.dumps(self.data_yarce))
            try:
                if a['data']: self.DB(a)
            except:
                pass

    def DB(self, data):
        pass