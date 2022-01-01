import sys
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from currency import Currency
from disk_io import JsonJob, XlsJob
from hh_parser import HhParser
from hh_request import Areas, HhRequest

RUR = '\u20bd'

# технологии, что мы запрашиваем в качестве ключевых слов
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
    'F#',
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
    'OpenCV',
    'OpenGL',
    'Perl',
    'PHP',
    'Python',
    'Qt',
    'Ruby',
    'Rust',
    'Scala',
    'Solidity',
    'SQL',
    'Swift',
    'TypeScript',
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


class Manager(object):

    def __init__(self) -> None:
        self._currency = Currency('rub')
        print(self._currency)
        self._set_saving_flag()

        # словарь с данными по вакансиям
        self._vacancies = []

        self._main()

    # выбор режима работы: запрос с сайта или с уже скачанных файлов
    def _set_saving_flag(self) -> None:
        while True:
            print('\rDo you want to request data from the hh.ru or download from files[y or n]? ', end='')
            ch = sys.stdin.read(1)
            if ch == 'y':
                self._saving_flag = True
                break
            elif ch == 'n':
                self._saving_flag = False
                break

    # TODO: написать функцию создающую словарь для сохранения в xls
    def _create_data_for_excel(salary, number, keyword):
        pass

    def _main(self):
        # цикл, перебора вакансий по списку ключевых слов
        for technology in technologies:
            self._vacancies.clear()
            if self._saving_flag is True:
                # получение данных по ключевому слову в вакансии и по локации работодателя
                self._vacancies = HhRequest(technology, Areas.MOSCOW).vacancies
                # сохранение в json созданный список с вакансиями
                JsonJob.save_data_to_json(self._vacancies, technology)
            else:
                # загрузка с json
                self._vacancies = JsonJob.get_data_from_json(technology)
            # вычисление средней ЗП и количество вакансий
            analyzed_vacancies = HhParser(self._vacancies, self._currency)
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
            # необязательная задержка, чтобы не нагружать сервисы hh
            time.sleep(0.25)

        XlsJob.save_data_to_xls(data_for_xls)
        Graph(data_for_xls)


class Graph(object):
    def __init__(self, data: dict) -> None:
        self._data = pd.DataFrame(data).sort_values(['Floor Salary'])

        self._show_graph()

    def _show_graph(self) -> None:
        x = np.arange(len(self._data['Technology']))
        plt.bar(x, height=self._data['Floor Salary'], width=0.5)
        plt.xticks(x, self._data['Technology'], rotation=60)
        plt.xlabel('Языки')
        plt.ylabel('Средняя ЗП, руб.')
        plt.title('Средние ЗП по языкам программирования')
        plt.grid(axis='y')
        plt.show()
