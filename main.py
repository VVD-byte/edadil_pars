from parser_lenta import pars_lenta
from parser_yarche import pars_yarche
from parser_bristol import pars_bristol
from parser_fixprice import pars_fixprice
from parser_perecr import pars_perecr

class start_pars:
    def start(self):
        pars_bristol().start_pars()

def main():
    a = start_pars()
    a.start()

if __name__ == '__main__':
    main()