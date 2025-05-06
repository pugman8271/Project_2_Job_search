import requests
import json
from src.HeadHunterAbstract import HeadHunterAbstract

class HeadHunterAPI(HeadHunterAbstract):
    """
    Класс для работы с API HeadHunter.

    Attributes:
        __HH_API_URL (str): URL API HeadHunter для получения вакансий.
    """

    __HH_API_URL = 'https://api.hh.ru/vacancies'

    def __get_vacancies(self, keyword='', per_page=50, salary=None):
        """
        Приватный метод для получения списка вакансий с HeadHunter.

        Args:
            keyword (str): Поисковой запрос.
            per_page (int): Количество элементов на странице.
            salary (int): Зарплата.

        Returns:
            list: Список вакансий в формате JSON или сообщение об ошибке.
        """
        params = {
            'text': keyword,  # Поисковой запрос
            'area': 1,  # Регион 1 - РФ
            'per_page': per_page,  # Количество элементов
            'salary': salary  # Зарплата
        }

        response = requests.get(self.__HH_API_URL, params=params)

        if response.status_code == 200:
            return response.json()['items']
        else:
            return f'Запрос не выполнен, ошибка: {response.status_code}'

    def get_vacancies(self, keyword='', per_page=20, salary=None):
        """
        Метод-обёртка для получения списка вакансий.

        Args:
            keyword (str): Поисковой запрос.
            per_page (int): Количество элементов на странице.
            salary (int): Зарплата.

        Returns:
            list: Список вакансий в формате JSON или сообщение об ошибке.
        """
        return self.__get_vacancies(keyword, per_page, salary)
