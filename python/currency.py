import requests
from bs4 import BeautifulSoup as bSoup


# ссылки на страницы с текущими курсами валют
USD_RUR = "https://www.google.com/search?q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%20%D0%BA%20%D1%80%D1%83%D0%B1%D0%BB%D1%8E"
EUR_RUR = "https://www.google.com/search?q=%D0%B5%D0%B2%D1%80%D0%BE%20%D0%BA%20%D1%80%D1%83%D0%B1%D0%BB%D1%8E"
# Заголовки для передачи вместе с URL
headers = {
  'User-Agent':
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}
# получение текущего курса доллара
def get_usd_price():
  # парсим всю страницу
  page = requests.get(USD_RUR, headers = headers)
  # проверяем что сервер отвечает
  if page.status_code == 403:
    print("Cannot get actual currency: HTTP 403 Forbidden")
    quit()
  # разбираем через BeautifulShop
  soup = bSoup(page.content, 'html.parser')
  # Находим нужное значение и возвращаем его
  text = soup.findAll("span", {"class": "DFlfde SwHCTb", "data-precision": 2})
  return float(text[0].text.replace(",", "."))

# получение текущего курса евро
def get_eur_price():
  # парсим всю страницу
  page = requests.get(EUR_RUR, headers = headers)
  # разбираем через BeautifulShop
  soup = bSoup(page.content, 'html.parser')
  # Находим нужное значение и возвращаем его
  text = soup.findAll("span", {"class": "DFlfde SwHCTb", "data-precision": 2})
  return float(text[0].text.replace(",", "."))