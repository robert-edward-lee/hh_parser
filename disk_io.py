import json
import os
from datetime import datetime as dt

import pandas as pd


class JsonJob(object):
    """Класс для работы с json файлами."""

    # функция сохранения вакансий в файл json
    @classmethod
    def save_data_to_json(cls, pages: list, name: str) -> None:
        if not os.path.exists('./docs'):
            os.mkdir('./docs')
        with open('./docs/{0}.jsonc'.format(name), 'w', encoding='utf-8') as json_file:
            json_file.write(json.dumps(pages, indent=2, ensure_ascii=False))

    # функция читающая вакансии json файлов
    @classmethod
    def get_data_from_json(cls, name: str) -> list:
        with open('./docs/{0}.jsonc'.format(name), 'r', encoding='utf-8') as json_file:
            file_contens = json_file.read()
        return json.loads(file_contens)


class XlsJob(object):
    """Класс для работы с xls файлами."""

    # функция сохранения DataFrame в файл xlsx
    @classmethod
    def save_data_to_xls(cls, data_for_xls: dict) -> None:
        # получение текущей даты
        date = dt.now()
        # сохранение данных в эксельку
        df = pd.DataFrame(data_for_xls)
        if not os.path.exists('./xls'):
            os.mkdir('./xls')
        df.to_excel(
            './xls/{0}.{1}.{2}_data.xlsx'.format(
                date.day,
                date.month,
                date.year,
            ),
            sheet_name='data',
        )
