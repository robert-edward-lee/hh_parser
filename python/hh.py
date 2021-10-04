# импортируем библиотеки
import requests
import pandas
import sys
import json
from datetime import datetime
# импорт модулей
import currency

# словарь с данными по вакансиям
vacancyList = []
# общая сумма средних зарплат по вакансиям
average_salary = 0
# количество вакансий
number_of_vacancies = 0
# символы валют
RUR = "\u20bd"
USD = "\u0024"
EUR = "\u20ac"
# языки, что мы запрашиваем в качестве ключевых слов
technologies = [
  "1С",
  "Assembler",
  "C",
  "C++",
  "C#",
  "Clojure",
  "Cuda",
  "Delphi",
  "Erlang",
  "F#",
  "Go",
  "Groovy",
  "Haskell",
  "Java",
  "JavaScript",
  "Kotlin",
  "Lisp",
  "Lua",
  "Matlab",
  "Objective-C",
  "OpenGL",
  "Perl",
  "PHP",
  "Python",
  "Ruby",
  "Rust",
  "Scala",
  "Solidity",
  "SQL",
  "Swift",
  "TypeScript",
  "Verilog"
]
# регионы с номерами согласно API hh.ru
areas = {
  "Moscow"              : 1,
  "Sankt-Petersburg"    : 2,
  "Voronezh"            : 26,
  "Russia"              : 113,
  "Moskovskaya oblast'" : 2019,
  "Krasnogorsk"         : 2034
}
# данные для передачи в эксельку
data_for_xls = {
  "Language"        : [],
  "Vacancy"         : [],
  "Average Salary"  : [],
  "Floor Salary"    : [],
  # условный коэффициент
  "Power"           : []
}
# функция получения данных по ключевому слову в вакансии и по локации работодателя
def getDataFromHh(key_word, area) -> list:
  # словарь с данными по вакансиям
  retVacancyList = []
  # запрос
  url = 'https://api.hh.ru/vacancies'
  # параметры, которые будут добавлены к запросу
  page = 0
  params = {'text': key_word, 'area': area, 'per_page': '100', 'page': page}
  # цикл, который скачивает вакансии
  for page in range(20):
    params['page'] = page
    pageObj = requests.get(url, params)
    # проверяем что сервер отвечает
    if pageObj.status_code < 200 or pageObj.status_code > 299:
      print("Cannot get actual currency! HTTP response code: %d"%pageObj.status_code)
      quit()
    elementOfVacancyList = pageObj.json()
    if not elementOfVacancyList['items']:
      break
    retVacancyList.append(elementOfVacancyList)
    # моднявое ожидание загрузки
    procents = page * 5
    print("\rGetting data for %s: %d%%"%(key_word, procents), end = '')
    if   procents % 4 == 0:
      print("   \r", end = '')
    elif procents % 4 == 1:
      print(".  \r", end = '')
    elif procents % 4 == 2:
      print(".. \r", end = '')
    else:
      print("...\r", end = '')
  return retVacancyList

# функция установки флага сохранения страниц в виде json
def setSavingFlag() -> bool:
  # запрос необходимости сохранения данных в файлы
  while 1:
    print("\rDo you want to request data from the hh.ru or download from files[y or n]? ", end = '')
    ch = sys.stdin.read(1)
    if ch == 'y':
      ret = True
      break
    elif ch == 'n':
      ret = False
      break
    else:
      continue
  return ret

# функция вычисления средней ЗП и количество вакансий
def getSalaryAndVacancies(vacancyList):
  total_average_salary = 0
  total_floor_salary = 0
  number_of_average_salaries = 0
  number_of_floor_salaries = 0
  # цикл, перебора по списку vacancyList, содержащий ответы на запросы к hh.ru
  for vacancy in vacancyList:
    # проверяем есть ли значения в словаре по ключу salary. Т.е проверяем есть ли в вакансии данные по зарплате
    if vacancy["salary"] != None:
      # записываем значение в переменную salary
      salary = vacancy["salary"]
      # проверяем есть ли значения по ключу from. Т.е проверяем есть ли в вакансии данные по минимальной зп
      if salary["from"] != None:
        # считаем количество обработанных вакансий в которых указана минимальная ЗП
        number_of_floor_salaries += 1
        # считаем сумму минимальной ЗП по вакансиям в зависимости от валюты
        if salary["currency"] == "USD":
          total_floor_salary += salary["from"] * USD_to_RUR
        elif salary["currency"] == "EUR":
          total_floor_salary += salary["from"] * EUR_to_RUR
        else:
          total_floor_salary += salary["from"]
        # проверяем есть ли значения по ключу to. Т.е проверяем есть ли в вакансии данные по максимальной зп
        if salary["to"] != None:
          # считаем количество обработанных вакансий в которых указана минимальная и максимальная ЗП
          number_of_average_salaries += 1
          # считаем сумму средней ЗП по вакансиям в зависимости от валюты
          if salary["currency"] == "USD":
            total_average_salary += ((salary["from"] + salary["to"]) / 2) * USD_to_RUR
          elif salary["currency"] == "EUR":
            total_average_salary += ((salary["from"] + salary["to"]) / 2) * EUR_to_RUR
          else:
            total_average_salary += (salary["from"] + salary["to"]) / 2
  # считаем средние арифметические значения, если это возможно
  if number_of_average_salaries != 0:
    ret_average_salary = total_average_salary / number_of_average_salaries
  else:
    ret_average_salary = 0
  if number_of_floor_salaries != 0:
    ret_floor_salary = total_floor_salary / number_of_floor_salaries
  else:
    ret_floor_salary = 0
  return int(ret_average_salary), int(ret_floor_salary), number_of_floor_salaries,

#
def getDataForExcel(salary, number, keyword):

  return

# функция сохранения вакансий в файл json
def saveDataToJson(pages, name) -> None:
  with open("./docs/%s.jsonc"%name, "w+", encoding = "utf-8") as file:
    file.write("[")
    for page in pages:
      for item in page["items"]:
        file.write("%s,"%(json.dumps(item, indent = 2, ensure_ascii = False)))
    # костыль! не могу удалить последнюю запятую и поэтому в конец файла записываю пустой элемент
    file.write("{ }]")
  return

# функция обрабатывающая вакансии уже сохраненные файлы
def getDataFromJson(name) -> list:
  data = []
  with open("./docs/%s.jsonc"%name) as file:
    file_contens = file.read()
  data = json.loads(file_contens)
  # костыль! удаляю последний элемент, т.е. он пусть подробности см. в saveDataToJson()
  data.pop()
  return data

# текущий курс валют
USD_to_RUR = currency.get_currency_price("usd")
EUR_to_RUR = currency.get_currency_price("eur")
print("Actual currency price: %s%.4f, %s%.4f"%(USD, USD_to_RUR, EUR, EUR_to_RUR))
flag_saving = setSavingFlag()
# цикл, перебора вакансий по списку ключевых слов
for technology in technologies:
  vacancyList.clear()
  average_salary = 0
  floor_salary = 0
  number_of_vacancies = 0
  if flag_saving == True:
    # получение данных по ключевому слову в вакансии и по локации работодателя
    vacancyList = getDataFromHh(technology, areas["Moscow"])
    # сохранение в json созданный список с вакансиями
    saveDataToJson(vacancyList, technology)
  # загрузка с json
  vacancyList = getDataFromJson(technology)
  # вычисление средней ЗП и количество вакансий
  average_salary, floor_salary, number_of_vacancies = getSalaryAndVacancies(vacancyList)
  # считаем среднюю ЗП, если это возможно, и заполняем данные для передачи в эксельку
  data_for_xls["Language"].append(technology)
  data_for_xls["Vacancy"].append(number_of_vacancies)
  data_for_xls["Average Salary"].append(average_salary)
  data_for_xls["Floor Salary"].append(floor_salary)
  # условный коэффициент,
  data_for_xls["Power"].append(floor_salary * number_of_vacancies / 1000000)
  if number_of_vacancies != 0:
    print("\rAfter processing %4d vacancies, I came to the conclusion that "
          "the average salary of a/an %12s developer is %s%6.0f, "
          "and floor salary is %s%6.0f"%(number_of_vacancies, technology, RUR, average_salary, RUR, floor_salary))
  else:
    print("\rAfter processing %4d vacancies, I came to the conclusion that "
          "a/an %s developer has nothing to do"%(number_of_vacancies, technology))
# получение текущей даты
date = datetime.now()
# сохранение данных в эксельку
df = pandas.DataFrame(data_for_xls)
df.to_excel("./%d.%d.%d_data.xlsx"%(date.day, date.month, date.year), sheet_name = "data")