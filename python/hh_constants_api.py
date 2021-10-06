"""Модуль с константами API hh.ru."""
from enum import Enum

url = 'https://api.hh.ru/vacancies'


class Areas(Enum):
    """Класс типа enum с кортежами, содержащими имена локации и номер в соответствии с API hh.ru."""

    MOSCOW = ('Moscow', 1)
    SAINT_PETERSBURG = ('Sankt-Peterburg', 2)
    VORONEZH = ('Voronezh', 26)
    RUSSIA = ('Russia', 113)
    MOSCOW_OBLAST = ('Moskovskaya oblast', 2019)
    RED_MOUNTAIN = ('Krasnogorsk', 2034)

    def __init__(self, _designation, _key) -> None:
        self._designation = _designation
        self._key = _key

    @property
    def designation(self) -> str:
        return self._designation

    @property
    def key(self) -> int:
        return self._key
