# импортируем библиотеки
import requests
import pandas
# словарь с данными по вакансиям
vacancyList = []
# общая сумма средних зарплат по вакансиям
total_salary = 0
# количество вакансий
number_of_vacancies = 0
# символ рубля
RUR = "\u20bd"
# текущий курс валют
USD_to_RUR = 72.88
EUR_to_RUR = 84.43
# языки, что мы запрашиваем в качестве ключевых слов
technologies = [
  '1С',
  'Assembler',
  'C',
  'C++',
  'C#',
  'Clojure',
  'Cuda',
  'Delphi',
  'Erlang',
  'Go',
  'Groovy',
  'Haskell',
  'Java',
  'JavaScript',
  'Kotlin',
  'Lisp',
  'Lua',
  'Matlab',
  'Objective-C',
  'OpenGL',
  'Perl',
  'PHP',
  'Python',
  'Ruby',
  'Rust',
  'Scala',
  'Solidity',
  'Swift',
  'SQL',
  'TypeScript',
  'Verilog',
  'VHDL',
  'Visual Basic'
]
# регионы с номерами согласно API hh.ru
areas = {
  'Moscow'          : 1,
  'Sankt-Petersburg': 2,
  'Voronezh'        : 26,
  'Russia'          : 113
}
# данные для передачи в эксельку
data_for_xls = {
  'Language'        : [],
  'Vacancy'         : [],
  'Salary'          : [],
  'Power'           : []
}
# запрос необходимости сохранения данных в файлы
print("Do you want save intermediate data in files [y]? ", end = '')
if input() == 'y':
  flag_saving = True
else:
  flag_saving = False
# цикл, перебора вакансий по списку ключевых слов
for technology in technologies:
  vacancyList.clear()
  total_salary = 0
  number_of_vacancies = 0
  # цикл, который скачивает вакансии
  for i in range(200):
    area = areas['Moscow']
    # запрос
    url = 'https://api.hh.ru/vacancies'
    # параметры, которые будут добавлены к запросу
    params = {'text': technology, 'area': area, 'per_page': '10', 'page': i}
    page = requests.get(url, params)
    # проверяем что сервер отвечает
    if page.status_code == 403:
      print("\rHTTP 403 Forbidden\t\t\t\t")
      quit()
    elementOfVacancyList = page.json()
    vacancyList.append(elementOfVacancyList)
    # моднявое ожидание загрузки
    print("\rProcessing for %s: %d%%"%(technology, i / 2), end = '')
    if   i % 3 == 0:
      print(".  ", end = '')
    elif i % 3 == 1:
      print(".. ", end = '')
    else:
      print("...", end = '')

  # сохраняем в файл созданный список с вакансиями, если это необходимо
  if flag_saving == True:
    f = open("./docs/%s.jsonc"%technology, "w+", encoding='utf-8')
    for vacancyDict in vacancyList:
      for key, val in vacancyDict.items():
        f.write("%s : %s\n"%(key, val))
    f.close()

  # цикл, перебора по списку vacancyList, содержащий ответы на запросы к hh.ru
  for j in vacancyList:
    items = j['items']
    # объявляем переменную n для подсчета, количества итераций цикла перебирающего зарплаты в вакансиях
    number_of_actual_vacancies = 0
    # объявляем переменную page_salary для подсчета, суммы зарплат в вакансиях на одной странице
    page_salary = 0
    # цикл, переберает объекты, т.е перебирает вакансии
    for i in items:
      # проверяем есть ли значения в словаре по ключу salary. Т.е проверяем есть ли в вакансии данные по зарплате
      # проверяем что валюта указана в рублях
      if i['salary'] != None:
        #записываем значение в переменную s
        salary = i['salary']
        # проверяем есть ли значения по ключу from. Т.е проверяем есть ли в вакансии данные по минимальной зп
        if salary['from'] != None and salary['to'] != None:
          # считаем количество обработанных вакансий в которых указана минимальная ЗП
          number_of_actual_vacancies += 1
          # получаем минимальную  и максимальную ЗП по ключу from
          # считаем сумму ЗП по вакансиям в зависимости от валюты
          if salary['currency'] == 'USD':
            page_salary += ((salary['from'] + salary['to']) / 2) * USD_to_RUR
          elif salary['currency'] == 'EUR':
            page_salary += ((salary['from'] + salary['to']) / 2) * EUR_to_RUR
          else:
            page_salary += (salary['from'] + salary['to']) / 2
    # добавляем сумму зп по итерации цикла одной страницы
    total_salary += page_salary
    # добавляем сумму n по итерации цикла одной страницы
    number_of_vacancies += number_of_actual_vacancies

  # считаем среднюю ЗП, если это возможно, и заполняем данные для передачи в эксельку
  data_for_xls['Language'].append(technology)
  data_for_xls['Vacancy'].append(number_of_vacancies)
  if number_of_vacancies != 0:
    average_salary = total_salary / number_of_vacancies
    data_for_xls['Salary'].append(average_salary)
    data_for_xls['Power'].append(average_salary * number_of_vacancies / 1000000)
    print("\rAfter processing %3d vacancies, I came to the conclusion that "
          "the average salary of a %12s developer is %s%6.0f"%(number_of_vacancies, technology, RUR, average_salary))
  else:
    data_for_xls['Salary'].append(0)
    data_for_xls['Power'].append(0)
    print("\rAfter processing %3d vacancies, I came to the conclusion that "
          "a %s developer has nothing to do"%(number_of_vacancies, technology))

# сохраняем данные в эксельку
df = pandas.DataFrame(data_for_xls)
df.to_excel('./data.xlsx', sheet_name = 1)