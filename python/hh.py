# импортируем библиотеки
import requests
import pandas
import sys
from datetime import datetime
from currency import get_eur_price
from currency import get_usd_price
# словарь с данными по вакансиям
vacancyList = []
# общая сумма средних зарплат по вакансиям
total_salary = 0
# количество вакансий
number_of_vacancies = 0
# символ рубля
RUR = "\u20bd"
# текущий курс валют
USD_to_RUR = get_usd_price()
EUR_to_RUR = get_eur_price()
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
  "Swift",
  "SQL",
  "TypeScript",
  "Verilog",
  "VHDL",
  "Visual Basic"
]
# регионы с номерами согласно API hh.ru
areas = {
  "Moscow"          : 1,
  "Sankt-Petersburg": 2,
  "Voronezh"        : 26,
  "Russia"          : 113
}
# данные для передачи в эксельку
data_for_xls = {
  "Language"        : [],
  "Vacancy"         : [],
  "Salary"          : [],
  "Power"           : []
}
# функция получения данных по ключевому слову в вакансии и по локации работодателя
def getDataFromHh(key_word, area):
  # словарь с данными по вакансиям
  retVacancyList = []
  # запрос
  url = 'https://api.hh.ru/vacancies'
  # параметры, которые будут добавлены к запросу
  page = 0
  params = {'text': key_word, 'area': area, 'per_page': '10', 'page': page}
  # цикл, который скачивает вакансии
  for page in range(200):
    params['page'] = page
    pageObj = requests.get(url, params)
    # проверяем что сервер отвечает
    if pageObj.status_code == 403:
      print("\rHTTP 403 Forbidden\t\t\t\t")
      quit()
    elementOfVacancyList = pageObj.json()
    if not elementOfVacancyList['items']:
      break
    retVacancyList.append(elementOfVacancyList)
    # моднявое ожидание загрузки
    print("\rProcessing for %s: %d%%"%(key_word, page / 2), end = '')
    if   page % 3 == 0:
      print(".  ", end = '')
    elif page % 3 == 1:
      print(".. ", end = '')
    else:
      print("...", end = '')
  return retVacancyList

# функция запроса необходимости сохранения страниц в виде json
def getSavingFlag():
  # запрос необходимости сохранения данных в файлы
  while 1:
    print("\rDo you want save intermediate data in files [y or n]? ", end = '')
    ch = input()
    if ch == 'y':
      ret = True
      break
    elif ch == 'n':
      ret = False
      break
    else:
      continue
    sys.stdout.flush()
  return ret

# функция вычисления средней ЗП и количество вакансий
def getSalaryAndVacancies(vacancyList):
  ret_salary = 0
  ret_number_of_vacancies = 0
  # цикл, перебора по списку vacancyList, содержащий ответы на запросы к hh.ru
  for j in vacancyList:
    items = j["items"]
    # объявляем переменную n для подсчета, количества итераций цикла перебирающего зарплаты в вакансиях
    number_of_actual_vacancies = 0
    # объявляем переменную page_salary для подсчета, суммы зарплат в вакансиях на одной странице
    page_salary = 0
    # цикл, переберает объекты, т.е перебирает вакансии
    for i in items:
      # проверяем есть ли значения в словаре по ключу salary. Т.е проверяем есть ли в вакансии данные по зарплате
      # проверяем что валюта указана в рублях
      if i["salary"] != None:
        #записываем значение в переменную s
        salary = i["salary"]
        # проверяем есть ли значения по ключу from. Т.е проверяем есть ли в вакансии данные по минимальной зп
        if salary["from"] != None and salary["to"] != None:
          # считаем количество обработанных вакансий в которых указана минимальная ЗП
          number_of_actual_vacancies += 1
          # получаем минимальную  и максимальную ЗП по ключу from
          # считаем сумму ЗП по вакансиям в зависимости от валюты
          if salary["currency"] == "USD":
            page_salary += ((salary["from"] + salary["to"]) / 2) * USD_to_RUR
          elif salary["currency"] == "EUR":
            page_salary += ((salary["from"] + salary["to"]) / 2) * EUR_to_RUR
          else:
            page_salary += (salary["from"] + salary["to"]) / 2
    # добавляем сумму зп по итерации цикла одной страницы
    ret_salary += page_salary
    # добавляем сумму n по итерации цикла одной страницы
    ret_number_of_vacancies += number_of_actual_vacancies
  return ret_salary, ret_number_of_vacancies

#
def getDataForExcel(salary, number, keyword):

  return

flag_saving = getSavingFlag()
# цикл, перебора вакансий по списку ключевых слов
for technology in technologies:
  vacancyList.clear()
  total_salary = 0
  number_of_vacancies = 0
  # получение данных по ключевому слову в вакансии и по локации работодателя
  vacancyList = getDataFromHh(technology, areas["Moscow"])
  # сохранение в файл созданный список с вакансиями, если это необходимо
  if flag_saving == True:
    f = open("./docs/%s.jsonc"%technology, "w+", encoding = "utf-8")
    for vacancyDict in vacancyList:
      for key, val in vacancyDict.items():
        f.write("%s : %s\n"%(key, val))
    f.close()
  # вычисление средней ЗП и количество вакансий
  total_salary, number_of_vacancies = getSalaryAndVacancies(vacancyList)
  # считаем среднюю ЗП, если это возможно, и заполняем данные для передачи в эксельку
  data_for_xls["Language"].append(technology)
  data_for_xls["Vacancy"].append(number_of_vacancies)
  if number_of_vacancies != 0:
    average_salary = total_salary / number_of_vacancies
    data_for_xls["Salary"].append(int(average_salary))
    data_for_xls["Power"].append(average_salary * number_of_vacancies / 1000000)
    print("\rAfter processing %3d vacancies, I came to the conclusion that "
          "the average salary of a %12s developer is %s%6.0f"%(number_of_vacancies, technology, RUR, average_salary))
  else:
    data_for_xls["Salary"].append(0)
    data_for_xls["Power"].append(0)
    print("\rAfter processing %3d vacancies, I came to the conclusion that "
          "a %s developer has nothing to do"%(number_of_vacancies, technology))
# получение текущей даты
date = datetime.now()
# сохранение данных в эксельку
df = pandas.DataFrame(data_for_xls)
df.to_excel("./%d.%d.%d_data.xlsx"%(date.day, date.month, date.year), sheet_name = "data")