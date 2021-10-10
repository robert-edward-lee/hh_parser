import json
import sys
import time
from datetime import datetime

import pandas
import requests
from currency import Currency
from hh_constants_api import Areas, url

# словарь с данными по вакансиям
vacancy_list = []
# символы валют
RUR = '\u20bd'
USD = '\u0024'
EUR = '\u20ac'

# языки, что мы запрашиваем в качестве ключевых слов
technologies = [
    # '1С',
    # 'Assembler',
    # 'C',
    # 'C++',
    # 'C#',
    # 'Clojure',
    # 'Cuda',
    # 'Delphi',
    'Erlang',
    # 'F#',
    # 'Go',
    # 'Groovy',
    # 'Haskell',
    # 'Java',
    # 'JavaScript',
    # 'Kotlin',
    # 'Lisp',
    # 'Lua',
    # 'Matlab',
    # 'Objective-C',
    # 'OpenGL',
    # 'Perl',
    # 'PHP',
    # 'Python',
    # 'Ruby',
    # 'Rust',
    # 'Scala',
    # 'Solidity',
    # 'SQL',
    # 'Swift',
    # 'TypeScript',
    # 'Verilog',
]

# данные для передачи в эксельку
data_for_xls = {
    'Language': [],
    'Vacancy': [],
    'Floor Salary': [],
    'Average Salary': [],
    'Ceiling Salary': [],
    # условный коэффициент
    'Power': [],
}


def get_data_from_hh(key_word: str, area: int) -> list:
    """Функция получения данных по ключевому слову в вакансии и по локации работодателя.

    Args:
        key_word (str): ключевое слово для поиска
        area (int): номер области поиска

    Returns:
        list: список вакансий
    """
    # словарь с данными по вакансиям
    ret_vacancy_list = []
    # параметры, которые будут добавлены к запросу
    page = 0
    request_params = {'text': key_word, 'area': area, 'per_page': '100', 'page': page}
    # цикл, который скачивает вакансии
    for page in range(20):
        request_params['page'] = page
        page_obj = requests.get(url, request_params)
        # проверяем что сервер отвечает
        if page_obj.status_code < 200 or page_obj.status_code > 299:
            print('Cannot get actual currency! HTTP response code: {0}'.format(page_obj.status_code))
            quit()
        element_of_vacancy_list = page_obj.json()
        if not element_of_vacancy_list['items']:
            break
        for item in element_of_vacancy_list['items']:
            ret_vacancy_list.append(item)
            # моднявое ожидание загрузки
            procents = page * 5
            print('\rGetting data for {0}: {1}%'.format(key_word, procents), end='')
            if procents % 4 == 0:
                print('   \r', end='')
            elif procents % 4 == 1:
                print('.  \r', end='')
            elif procents % 4 == 2:
                print('.. \r', end='')
            else:
                print('...\r', end='')
    return ret_vacancy_list


def set_saving_flag() -> bool:
    """Функция установки флага сохранения страниц в виде json.

    Returns:
        bool: флаг
    """
    # запрос необходимости сохранения данных в файлы
    while True:
        print('\rDo you want to request data from the hh.ru or download from files[y or n]? ', end='')
        ch = sys.stdin.read(1)
        if ch == 'y':
            ret = True
            break
        elif ch == 'n':
            ret = False
            break
    return ret


def get_salary_and_vacancies(data_list: list) -> tuple:
    """Функция вычисления средней ЗП и количество вакансий.

    Args:
        data_list (list): список вакансий

    Returns:
        tuple: средняя макс. ЗП, средняя мин. ЗП, кол-во вакансий
    """
    # общее сумма минимальных и максимальных ЗП
    total_floor_salary = 0
    total_ceiling_salary = 0
    # число вакансий содержащих минимальные и максимальные ЗП
    number_of_floor_salaries = 0
    number_of_ceiling_salaries = 0
    # возвращаемые значения:
    #   средняя максимальная ЗП,
    #   средняя минимальная ЗП,
    #   общее число вакансий на рынке (не более 2000)
    ret_ceiling_salary = 0
    ret_floor_salary = 0
    ret_number_of_vacancies = 0
    # цикл, перебора по списку data_list, содержащий ответы на запросы к hh.ru
    for ret_number_of_vacancies, vacancy in enumerate(data_list):
        # считаем общее число вакансий ret_number_of_vacancies += 1
        # проверяем есть ли значения в словаре по ключу salary. Т.е проверяем есть ли в вакансии данные по зарплате
        if vacancy['salary'] is not None:
            # записываем значение в переменную salary
            salary = vacancy['salary']
            # проверяем есть ли значения по ключу from. Т.е проверяем есть ли в вакансии данные по минимальной зп
            if salary['from'] is not None:
                # считаем количество обработанных вакансий в которых указана минимальная ЗП
                number_of_floor_salaries += 1
                # считаем сумму минимальной ЗП по вакансиям в зависимости от валюты
                if salary['currency'] == 'USD':
                    total_floor_salary += salary['from'] * USD_to_RUR
                elif salary['currency'] == 'EUR':
                    total_floor_salary += salary['from'] * EUR_to_RUR
                else:
                    total_floor_salary += salary['from']
            # проверяем есть ли значения по ключу to. Т.е проверяем есть ли в вакансии данные по максимальной зп
            if salary['to'] is not None:
                # считаем количество обработанных вакансий в которых указана минимальная и максимальная ЗП
                number_of_ceiling_salaries += 1
                # считаем сумму средней ЗП по вакансиям в зависимости от валюты
                if salary['currency'] == 'USD':
                    total_ceiling_salary += salary['to'] * USD_to_RUR
                elif salary['currency'] == 'EUR':
                    total_ceiling_salary += salary['to'] * EUR_to_RUR
                else:
                    total_ceiling_salary += salary['to']
    # считаем средние арифметические значения, если это возможно
    try:
        ret_ceiling_salary = total_ceiling_salary // number_of_ceiling_salaries
    except ZeroDivisionError:
        print('Number of the vacancies with maximal salary is null')
    try:
        ret_floor_salary = total_floor_salary // number_of_floor_salaries
    except ZeroDivisionError:
        print('Number of the vacancies with minimal salary is null')
    return ret_ceiling_salary, ret_floor_salary, ret_number_of_vacancies


def get_data_for_excel(salary, number, keyword):
    return


def save_data_to_json(pages, name) -> None:
    """Функция сохранения вакансий в файл json.

    Args:
        pages (dict): данные с вакансиями
        name (str): имя файла
    """
    with open('./docs/{0}.jsonc'.format(name), 'w+', encoding='utf-8') as json_file:
        json_file.write(json.dumps(pages, indent=2, ensure_ascii=False))


def get_data_from_json(name: str) -> list:
    """Функция читающая вакансии json файлов.

    Args:
        name (str): имя файла

    Returns:
        list: список вакансий
    """
    with open('./docs/{0}.jsonc'.format(name), encoding='utf-8') as json_file:
        file_contens = json_file.read()
    return json.loads(file_contens)


# текущий курс валют
current_rate = Currency()
USD_to_RUR = current_rate.usd
EUR_to_RUR = current_rate.eur
print('Actual currency price: {0}{1:.4f}, {2}{3:.4f}'.format(USD, USD_to_RUR, EUR, EUR_to_RUR))
flag_saving = set_saving_flag()
# цикл, перебора вакансий по списку ключевых слов
for technology in technologies:
    vacancy_list.clear()
    floor_salary = 0
    ceiling_salary = 0
    number_of_vacancies = 0
    if flag_saving is True:
        # получение данных по ключевому слову в вакансии и по локации работодателя
        vacancy_list = get_data_from_hh(technology, Areas.MOSCOW.key)
        # сохранение в json созданный список с вакансиями
        save_data_to_json(vacancy_list, technology)
    # загрузка с json
    vacancy_list = get_data_from_json(technology)
    # вычисление средней ЗП и количество вакансий
    ceiling_salary, floor_salary, number_of_vacancies = get_salary_and_vacancies(vacancy_list)
    # считаем среднюю ЗП, и заполняем данные для передачи в эксельку
    data_for_xls['Language'].append(technology)
    data_for_xls['Vacancy'].append(number_of_vacancies)
    data_for_xls['Floor Salary'].append(floor_salary)
    data_for_xls['Average Salary'].append((floor_salary + ceiling_salary) // 2)
    data_for_xls['Ceiling Salary'].append(ceiling_salary)
    # условный коэффициент
    data_for_xls['Power'].append(floor_salary * number_of_vacancies / 1000000)
    print('\rAfter processing {0:>4} vacancies in {1}, I came to the conclusion that '.format(
        number_of_vacancies, Areas.MOSCOW.designation,
    ), end='')
    if number_of_vacancies != 0:
        print('the salary of a/an {0:>11} developer is from {1}{2:>6}, to {3}{4:>6}'.format(
            technology, RUR, floor_salary, RUR, ceiling_salary,
        ))
    else:
        print('a/an {:>11} developer has nothing to do'.format(technology))
    # Необязательная задержка, чтобы не нагружать сервисы hh
    time.sleep(0.25)
# получение текущей даты
date = datetime.now()
# сохранение данных в эксельку
df = pandas.DataFrame(data_for_xls)
df.to_excel('./{0}.{1}.{2}_data.xlsx'.format(date.day, date.month, date.year), sheet_name='data')
