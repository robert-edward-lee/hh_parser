import json
from datetime import datetime as dt

import pandas as pd


# функция сохранения вакансий в файл json
def save_data_to_json(pages: list, name: str) -> None:
    with open('./docs/{0}.jsonc'.format(name), 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(pages, indent=2, ensure_ascii=False))


# функция читающая вакансии json файлов
def get_data_from_json(name: str) -> list:
    with open('./docs/{0}.jsonc'.format(name), 'r', encoding='utf-8') as json_file:
        file_contens = json_file.read()
    return json.loads(file_contens)


# функция сохранения DataFrame в файл xlsx
def save_data_to_xlsx(data_for_xls: dict) -> None:
    # получение текущей даты
    date = dt.now()
    # сохранение данных в эксельку
    df = pd.DataFrame(data_for_xls)
    df.to_excel(
        './{0}.{1}.{2}_data.xlsx'.format(
            date.day,
            date.month,
            date.year,
        ),
        sheet_name='data',
    )
