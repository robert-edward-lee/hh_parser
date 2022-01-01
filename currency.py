import requests
from bs4 import BeautifulSoup as bSoup

# символы валют в юникоде
EUR = '\u20ac'
RUR = '\u20bd'
USD = '\u0024'

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
            'eur', 'rub', 'usd'
    """

    _currencies = {
        'eur': {'symbol': EUR, 'price': 0.0},
        'rub': {'symbol': RUR, 'price': 0.0},
        'usd': {'symbol': USD, 'price': 0.0},
    }

    def __init__(self, base_currency: str) -> None:
        self._base_currency = base_currency

        for currency in self._currencies:
            if currency != self._base_currency:
                self._currencies[currency]['price'] = self._get_currency_price(currency)
                setattr(self, currency, lambda: self._currencies[currency]['price'])

    # получение текущего курса
    def _get_currency_price(self, currency: str) -> float:
        url = 'https://ru.investing.com/currencies/{0}-{1}'.format(currency, self._base_currency)
        # парсим всю страницу
        page_obj = requests.get(url, headers=main_header)
        page_obj.raise_for_status()
        # разбираем через BeautifulShop
        soup = bSoup(page_obj.content, 'html.parser')
        # находим нужное значение и возвращаем его
        text = soup.findAll('span', {'data-test': 'instrument-price-last'})
        return float(text[0].text.replace(',', '.'))

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
