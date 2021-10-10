import json
import os
import time

import requests

# Получаем перечень ранее созданных файлов со списком вакансий и проходимся по нему в цикле
for fl in os.listdir('./docs/pagination'):
    # Открываем файл, читаем его содержимое, закрываем файл
    with open('./docs/pagination/{0}'.format(fl), encoding='utf8') as f:
        jsonText = f.read()
    # Преобразуем полученный текст в объект справочника
    jsonObj = json.loads(jsonText)
    # Получаем и проходимся по непосредственно списку вакансий
    for v in jsonObj['items']:
        # Обращаемся к API и получаем детальную информацию по конкретной вакансии
        req = requests.get(v['url'])
        data = req.content.decode()
        req.close()
        # Создаем файл в формате json с идентификатором вакансии в качестве названия
        # Записываем в него ответ запроса и закрываем файл
        fileName = './docs/vacancies/{0}.json'.format(v['id'])
        with open(fileName, mode='w', encoding='utf8') as f:
            f.write(data)
        time.sleep(0.25)
print('Вакансии собраны')
