from parser import pars
import json
import logging
from bs4 import BeautifulSoup

class pars_perecr(pars):
    def __init__(self):
        super().__init__()
        self.url = 'https://www.vprok.ru'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        }
        self.rub = {}

    def start_pars_(self):
        for i in self.get_soup(self.url).find_all('a', {'class':'xf-catalog-categories__link'}):
            self.rub[i.text.replace('  ', '').replace('\n', '')] = {}
            try:
                for j in self.get_soup('https://www.vprok.ru' + i.get('href')).find_all('a', {'class':'xf-filter__item-label xf-ripple js-xf-ripple xf-ripple_gray'}):
                    self.rub[i.text.replace('  ', '').replace('\n', '')][j.text.replace('  ', '').replace('\n', '')] = {}
                    try:
                        for q in self.get_soup('https://www.vprok.ru' + j.get('href')).find_all('a', {'class':'xf-filter__item-label xf-ripple js-xf-ripple xf-ripple_gray'}):
                            self.rub[i.text.replace('  ', '').replace('\n', '')][j.text.replace('  ', '').replace('\n', '')][q.text.replace('  ', '').replace('\n', '')] = {}
                            self.rub[i.text.replace('  ', '').replace('\n', '')][j.text.replace('  ', '').replace('\n', '')][q.text.replace('  ', '').replace('\n', '')]['src'] = q.get('href')
                    except:
                        self.rub[i.text.replace('  ', '').replace('\n', '')][j.text.replace('  ', '').replace('\n', '')]['src'] = j.get('href')
            except:
                self.rub[i.text.replace('  ', '').replace('\n', '')]['src'] = i.get('href')
        print(self.rub)
        with open('q.json', 'w', encoding = 'utf-8') as t:
            t.write(json.dumps(self.rub))

    def start_pars(self):
        for i in self.get_soup(self.url).find_all('span', {'class':'xf-menu__item-text'}):
            print(i.text.replace('  ', '').replace('\n', ''))
        print(len(self.get_soup(self.url).find_all('span', {'class':'xf-menu__item-text'})))

    def get_soup(self, url):
        a = self.requests_get(url, self.headers)
        with open('a.txt', 'w') as t:
            t.write(a)
        return BeautifulSoup(a, 'lxml')