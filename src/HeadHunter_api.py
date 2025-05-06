import requests
from src.HeadHunterAbstract import HeadHunterAbstract


class HeadHunterAPI(HeadHunterAbstract):
    """
    Класс для работы с API HeadHunter.
    """

    __HH_API_URL = 'https://api.hh.ru/vacancies'

    def __get_vacancies(self, keyword: str = '', per_page: int = 50, salary: int | None = None) -> list | str:
        """
        Приватный метод для получения списка вакансий с HeadHunter.
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

    def get_vacancies(self, keyword: str = '', per_page: int = 20, salary: int | None = None) -> list | str:
        """
        Метод-обёртка для получения списка вакансий.
        """
        return self.__get_vacancies(keyword, per_page, salary)
