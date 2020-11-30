from parser_lenta import pars_lenta
from parser_yarche import pars_yarche
from parser_fixprice import pars_fixprice

class start_pars:
    def start(self):
        pars_fixprice().start_pars()

def main():
    a = start_pars()
    a.start()

if __name__ == '__main__':
    main()