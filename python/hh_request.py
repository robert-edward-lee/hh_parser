from enum import Enum

import requests as rq

URL = 'https://api.hh.ru/vacancies'
NUMBER_OF_PAGES = 20
VACANCIES_PER_PAGE = 100


class Areas(Enum):
    """Класс типа enum с кортежами, содержащими имена локации и номер в соответствии с API hh.ru."""

    MOSCOW = ('Moscow', 1)
    SAINT_PETERSBURG = ('Sankt-Peterburg', 2)
    VORONEZH = ('Voronezh', 26)
    RUSSIA = ('Russia', 113)
    MOSCOW_OBLAST = ('Moskovskaya oblast', 2019)
    RED_MOUNTAIN = ('Krasnogorsk', 2034)

    def __init__(self, _title, _key) -> None:
        self._title = _title
        self._key = _key

    @property
    def title(self) -> str:
        return self._title

    @property
    def key(self) -> int:
        return self._key


class HhRequest(object):
    """Класс получающий список вакансий по ключевому слову и региону."""

    def __init__(self, key_word: str, area: Areas) -> None:
        self._area = area
        self._request_params = {
            'text': key_word,
            'area': self._area.key,
            'per_page': str(VACANCIES_PER_PAGE),
            'page': 0,
        }
        self._vacancy_list = self._get_data_from_hh()

    @property
    def vacancies(self) -> list:
        return self._vacancy_list

    # функция получения данных по ключевому слову в вакансии и по локации работодателя
    def _get_data_from_hh(self) -> list:
        # словарь с данными по вакансиям
        ret_vacancy_list = []
        # цикл, который скачивает вакансии
        for page_number in range(NUMBER_OF_PAGES):
            self._request_params['page'] = page_number
            # попытка получить ответ
            page_obj = rq.get(URL, self._request_params)
            page_obj.raise_for_status()
            # преобразование в словарь методом json()
            element_of_vacancy_list = page_obj.json()
            # проверка на наличие вакансий
            if not element_of_vacancy_list['items']:
                break
            # создание списка вакансий без метаданных класса requests.models.Response
            for vacancy in element_of_vacancy_list['items']:
                ret_vacancy_list.append(vacancy)
                # моднявое ожидание загрузки
                self._progress_bar()
        return ret_vacancy_list

    # моднявое ожидание загрузки
    def _progress_bar(self) -> None:
        # моднявое ожидание загрузки
        procents = (100 * self._request_params['page']) // NUMBER_OF_PAGES
        print(
            'Getting data for {0} in {1}: {2}%'.format(
                self._request_params['text'],
                self._area.title,
                procents,
            ),
            end='',
        )
        if procents % 4 == 0:
            print('   \r', end='')
        elif procents % 4 == 1:
            print('.  \r', end='')
        elif procents % 4 == 2:
            print('.. \r', end='')
        else:
            print('...\r', end='')
