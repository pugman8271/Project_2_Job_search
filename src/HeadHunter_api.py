import requests
import json
from src.HeadHunterAbstract import HeadHunterAbstract

class HeadHunterAPI(HeadHunterAbstract):
    HH_API_URL = 'https://api.hh.ru/vacancies'

    def get_vacancies(self, keyword='', per_page=20, salary=None):
        params = {
            'text': keyword,  # Поисковой запрос
            'area': 1,  # Регион 1 - РФ
            'per_page': per_page,  # Количество элементов
            'salary': salary  # Зарплата
        }

        response = requests.get(self.HH_API_URL, params=params)

        if response.status_code == 200:
            # with open('data/all_vacancy_tst.json', 'w', encoding='utf-8') as file:
            #     json.dump(response.json()['items'], file, ensure_ascii=False, indent=2)
            #
            return response.json()['items']
        else:
            return f'Запрос не выполнен, ошибка: {response.status_code}'
