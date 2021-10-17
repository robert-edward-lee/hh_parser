import sys
import time

import disk_io
from currency import Currency
from hh_parser import HhParser
from hh_request import Areas, HhRequest

# словарь с данными по вакансиям
vacancies = []

RUR = '\u20bd'

# технологии, что мы запрашиваем в качестве ключевых слов
technologies = [
    '1С',
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
    'Verilog',
]

# данные для передачи в эксельку
data_for_xls = {
    'Technology': [],
    'Number of vacancies': [],
    'Floor Salary': [],
    'Average Salary': [],
    'Ceiling Salary': [],
    # условный коэффициент
    'Power': [],
}


# выбор режима работы: запрос с сайта или с уже скачанных файлов
def set_saving_flag() -> bool:
    while True:
        print('\rDo you want to request data from the hh.ru or download from files[y or n]? ', end='')
        ch = sys.stdin.read(1)
        if ch == 'y':
            flag = True
            break
        elif ch == 'n':
            flag = False
            break
    return flag


def get_data_for_excel(salary, number, keyword):
    pass


currency = Currency()
flag_saving = set_saving_flag()
# цикл, перебора вакансий по списку ключевых слов
for technology in technologies:
    vacancies.clear()
    if flag_saving is True:
        # получение данных по ключевому слову в вакансии и по локации работодателя
        vacancies = HhRequest(technology, Areas.MOSCOW).vacancies
        # сохранение в json созданный список с вакансиями
        disk_io.save_data_to_json(vacancies, technology)
    else:
        # загрузка с json
        vacancies = disk_io.get_data_from_json(technology)
    # вычисление средней ЗП и количество вакансий
    analyzed_vacancies = HhParser(vacancies, currency)
    # считаем среднюю ЗП, и заполняем данные для передачи в эксельку
    data_for_xls['Technology'].append(technology)
    data_for_xls['Number of vacancies'].append(analyzed_vacancies.number_of_vacancies)
    data_for_xls['Floor Salary'].append(analyzed_vacancies.floor_salary)
    data_for_xls['Average Salary'].append(analyzed_vacancies.average_salary)
    data_for_xls['Ceiling Salary'].append(analyzed_vacancies.ceiling_salary)
    # условный коэффициент
    data_for_xls['Power'].append(analyzed_vacancies.power)
    print(
        '\rAfter processing {0:>4} vacancies in {1}, I came to the conclusion that '.format(
            analyzed_vacancies.number_of_vacancies,
            Areas.MOSCOW.title,
        ),
        end='',
    )
    if analyzed_vacancies.number_of_vacancies == 0:
        print('a/an {0:>11} developer has nothing to do'.format(technology))

    else:
        print(
            'the salary of a/an {0:>11} developer is from {1}{2:>6}, to {3}{4:>6}'.format(
                technology,
                RUR,
                analyzed_vacancies.floor_salary,
                RUR,
                analyzed_vacancies.ceiling_salary,
            ),
        )
    # Необязательная задержка, чтобы не нагружать сервисы hh
    time.sleep(0.25)

disk_io.save_data_to_xlsx(data_for_xls)
