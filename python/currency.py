import requests
from bs4 import BeautifulSoup as bSoup

# Заголовки для передачи вместе с URL
main_header = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/93.0.4577.99 Safari/537.36',
}


class Currency(object):
    """Класс для получения текущего курса валют, в частности доллара и евро."""

    def __init__(self) -> None:
        self._usd = self._get_currency_price('usd')
        self._eur = self._get_currency_price('eur')

    @property
    def usd(self) -> float:
        return self._usd

    @property
    def eur(self) -> float:
        return self._eur

    # получение текущего курса доллара
    def _get_currency_price(self, currency) -> float:
        url = 'https://ru.investing.com/currencies/{0}-rub'.format(currency)
        # парсим всю страницу
        page_obj = requests.get(url, headers=main_header)
        # проверяем что сервер отвечает
        if page_obj.status_code < 200 or page_obj.status_code > 299:
            print('Unable to get the currencies rate! HTTP response code: {0}'.format(page_obj.status_code))
            quit()
        # разбираем через BeautifulShop
        soup = bSoup(page_obj.content, 'html.parser')
        # Находим нужное значение и возвращаем его
        text = soup.findAll('span', {'id': 'last_last'})
        return float(text[0].text.replace(',', '.'))
