# импортируем библиотеку request для работы с данными в сети
import requests
vacancyList = []
total_salary = 0
number_of_vacancy = 0
RUR = "\u20bd"
USD_to_RUR = 72.88
EUR_to_RUR = 84.43
#языки, что мы запрашиваем
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
# technologies = ['Assembler']
#регионы
areas = {
  'Moscow'          : 1,
  'Sankt-Petersburg': 2,
  'Voronezh'        : 26,
  'Russia'          : 113
  }
#цикл, перебора языков программирования
for technology in technologies:
  vacancyList.clear()
  total_salary = 0
  number_of_vacancy = 0
  #цикл, который скачивает вакансии
  for i in range(200):
    area = areas.get('Moscow')
    # запрос
    url = 'https://api.hh.ru/vacancies'
    #параметры, которые будут добавлены к запросу
    params = {'text': technology, 'area': area, 'per_page': '10', 'page': i}
    page = requests.get(url, params)
    if page.status_code == 403:
      print("\rHTTP 403 Forbidden\t\t\t\t")
      quit()
    elementOfVacancyList = page.json()
    vacancyList.append(elementOfVacancyList)
    print("\rProcessing for %s: %d%%"%(technology, i / 2), end = '')
  # print("\r     \r", end = '')

  # #сохраняем в файл
  f = open("./docs/%s.jsonc"%technology, "w+")
  for vacancyDict in vacancyList:
    for key, val in vacancyDict.items():
      f.write("%s : %s\n"%(key, val))
  f.close()

  #цикл, перебора по списку vacancyList, содержащий ответы на запросы к hh.ru
  for j in vacancyList:
    y = j['items']
    #объявляем переменную n для подсчета, количества итераций цикла перебирающего зарплаты в вакансиях
    n = 0
    #объявляем переменную sum_zp для подсчета, суммы зарплат в вакансиях
    sum_zp = 0
    #цикл, переберает объекты, т.е перебирает вакансии
    for i in y:
      # проверяем есть ли значения в словаре по ключу salary. Т.е проверяем есть ли в вакансии данные по зарплате
      # проверяем что валюта указана в рублях
      if i['salary'] != None:
        #записываем значение в переменную s
        salary = i['salary']
        # проверяем есть ли значения по ключу from. Т.е проверяем есть ли в вакансии данные по минимальной зп
        if salary['from'] != None and salary['to'] != None:
          # считаем количество обработанных вакансий в которых указана минимальная ЗП
          n += 1
          # #получаем минимальную  и максимальную ЗП по ключу from
          # salary['from']
          # salary['to']
          #считаем сумму ЗП по вакансиям
          if salary['currency'] == 'USD':
            sum_zp += ((salary['from'] + salary['to']) / 2) * USD_to_RUR
          elif salary['currency'] == 'EUR':
            sum_zp += ((salary['from'] + salary['to']) / 2) * EUR_to_RUR
          else:
            sum_zp += (salary['from'] + salary['to']) / 2
    #добавляем сумму зп по итерации цикла
    total_salary += sum_zp
    #добавляем сумму n по итерации цикла
    number_of_vacancy += n
  #считаем среднюю ЗП
  if number_of_vacancy != 0:
    average_salary = total_salary / number_of_vacancy
    print("\rAfter processing %3d vacancies, I came to the conclusion that "
          "the average salary of a %12s developer is %s%6.0f"%(number_of_vacancy, technology, RUR, average_salary))
  else:
    print("\rAfter processing %3d vacancies, I came to the conclusion that "
          "a %s developer has nothing to do"%(number_of_vacancy, technology))