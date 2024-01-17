import mureq
from bs4 import BeautifulSoup as bSoup

# символы валют в юникоде
AZN = '\u20BC'
EUR = '\u20ac'
KZT = '\u20B8'
RUB = '\u20bd'
UAH = '\u20b4'
USD = '\u0024'
BYN = 'Br'

# заголовки для передачи вместе с URL
main_header = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        + 'Chrome/93.0.4577.99 Safari/537.36'
    ),
}


class Currency(object):
    """Класс для получения текущего курса валют. На вход передаётся название валюты, в цене которой формируются цены
    остальных валют

    Поддерживаемые валюты:
            `eur`, `rub`, `uah`, `usd`, `kzt`, `azt`
    """

    _currencies = {
        'eur': {'symbol': EUR, 'price': 1},
        'rub': {'symbol': RUB, 'price': 1},
        'uah': {'symbol': UAH, 'price': 1},
        'usd': {'symbol': USD, 'price': 1},
        'kzt': {'symbol': KZT, 'price': 1},
        'azn': {'symbol': AZN, 'price': 1},
        'byn': {'symbol': BYN, 'price': 1},
    }

    def __init__(self, base_currency: str) -> None:
        self._base_currency = base_currency

        for currency in self._currencies:
            setattr(self, currency, lambda: self._currencies[currency]['price'])
            if currency != self._base_currency:
                self._currencies[currency]['price'] = self._get_currency_price(currency)

    def __str__(self) -> str:
        ret_str = 'Actual currency price:'
        for currency in self._currencies:
            if currency != self._base_currency:
                ret_str += '\n\t{0}1 = {1}{2:.4f}'.format(
                    self._currencies[currency]['symbol'],
                    self._currencies[self._base_currency]['symbol'],
                    self._currencies[currency]['price'],
                )
        return ret_str

    # получение текущего курса
    def _get_currency_price(self, currency: str) -> float:
        url = 'https://ru.investing.com/currencies/{0}-{1}'.format(currency, self._base_currency)
        # парсим всю страницу
        page_obj = mureq.get(url, headers=main_header)
        page_obj.raise_for_status()
        # разбираем через BeautifulShop
        soup = bSoup(page_obj.content, 'html.parser')
        # находим нужное значение и возвращаем его
        text = soup.findAll(attrs={'data-test': 'instrument-price-last'})[0].text
        return float(text.replace(',', '.'))

    def get_current_value(self, currency: str) -> float:
        try:
            return self._currencies[currency]['price']
        except KeyError:
            raise ValueError('Unknown currency: {0}'.format(currency))
