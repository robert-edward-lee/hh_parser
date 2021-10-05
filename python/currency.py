import requests
from bs4 import BeautifulSoup as bSoup

# ссылки на страницы с текущими курсами валют
url_invest = "https://ru.investing.com/currencies/"
# Заголовки для передачи вместе с URL
main_header = {
  "User-Agent":
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.99 Safari/537.36"
}

class Currency(object):
  """Класс для получения текущего курса валют, в частности доллара и евро"""
  usd = 0.0
  """Стоимость доллара в рублях"""
  eur = 0.0
  """Стоимость евро в рублях"""

  def __init__(self) -> None:
    self.usd = self._get_currency_price("usd")
    self.eur = self._get_currency_price("eur")

  # получение текущего курса доллара
  def _get_currency_price(self, currency) -> float:
    url = url_invest + currency + "-rub"
    # парсим всю страницу
    pageObj = requests.get(url, headers = main_header)
    # проверяем что сервер отвечает
    if pageObj.status_code < 200 or pageObj.status_code > 299:
      print("Unable to get the current %s rate! HTTP response code: %d"%(currency, pageObj.status_code))
      quit()
    # разбираем через BeautifulShop
    soup = bSoup(pageObj.content, "html.parser")
    # Находим нужное значение и возвращаем его
    text = soup.findAll("span", {"id": "last_last"})
    return float(text[0].text.replace(",", "."))