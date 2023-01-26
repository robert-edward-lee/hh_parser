from statistics import StatisticsError, median

from currency import Currency

NORMALIZING_FACTOR = 0.000001


class HhParser(object):
    """Класс разбирающий инфу из вакансии."""

    def __init__(self, vacancies_list: list, currency: Currency) -> None:
        self._vacancies_list = vacancies_list
        # список минимальных и максимальных ЗП
        self._list_floor_salary = []
        self._list_ceiling_salary = []
        # текущий курс валют
        self._current_rate = currency

        self._number_of_vacancies = len(vacancies_list)

        self._get_salary()
        try:
            self._floor_salary = int(median(self._list_floor_salary))
        except StatisticsError:
            self._floor_salary = 0
        try:
            self._ceiling_salary = int(median(self._list_ceiling_salary))
        except StatisticsError:
            self._ceiling_salary = 0
        self._average_salary = (self._floor_salary + self._ceiling_salary) // 2

    @property
    def number_of_vacancies(self) -> int:
        return self._number_of_vacancies

    @property
    def floor_salary(self) -> int:
        return self._floor_salary

    @property
    def ceiling_salary(self) -> int:
        return self._ceiling_salary

    @property
    def average_salary(self) -> int:
        return self._average_salary

    @property
    def power(self) -> float:
        return self._floor_salary * self._number_of_vacancies * NORMALIZING_FACTOR

    # функция вычисления средней медианной ЗП и количества вакансий.
    def _get_salary(self) -> tuple:
        # цикл, перебора по списку data_list, содержащий ответы на запросы к hh.ru
        for vacancy in self._vacancies_list:
            self._salary_analysis(vacancy['salary'])

    # функция проверки поля salary вакансии
    def _salary_analysis(self, salary: dict) -> None:
        # проверяем есть ли в вакансии данные по минимальной зп
        if salary['from'] is not None:
            # считаем сумму минимальной ЗП по вакансиям в зависимости от валюты
            self._list_floor_salary.append(
                self._get_local_salary(
                    salary=salary['from'],
                    currency=salary['currency'],
                ),
            )
        # проверяем есть ли в вакансии данные по максимальной зп
        if salary['to'] is not None:
            # считаем сумму средней ЗП по вакансиям в зависимости от валюты
            self._list_ceiling_salary.append(
                self._get_local_salary(
                    salary=salary['to'],
                    currency=salary['currency'],
                ),
            )

    # получение ЗП в местной валюте (рублях)
    def _get_local_salary(self, salary, currency) -> int:
        ret_salary = 0
        if currency == 'RUR':
            ret_salary = salary
        else:
            ret_salary = salary * self._current_rate.get_current_value(currency.lower())
        return ret_salary
