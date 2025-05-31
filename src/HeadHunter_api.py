import requests

from src.HeadHunterAbstract import HeadHunterAbstract


class HeadHunterAPI(HeadHunterAbstract):
    """
    Класс для работы с API HeadHunter.
    """

    __HH_API_URL = "https://api.hh.ru/vacancies"

    def __init__(self):
        self.name = None

    def __get_vacancies(
        self, keyword: str = "", per_page: int = 50, salary: int | None = None
    ) -> list | str:
        """
        Приватный метод для получения списка вакансий с HeadHunter.
        """
        params = {
            "text": keyword,  # Поисковой запрос
            "area": 1,  # Регион 1 - РФ
            "per_page": per_page,  # Количество элементов
            "salary": salary,  # Зарплата
        }

        response = requests.get(self.__HH_API_URL, params=params)

        if response.status_code == 200:
            return response.json()["items"]
        else:
            return f"Запрос не выполнен, ошибка: {response.status_code}"



    def get_request_employers(self):
        """
        Метод возвращающий json по умолчанию 10 компаний
        """
        list_employeers = []
        if self.name is None:
            params = {
                "per_page": 10,
                "sort_by": "by_vacancies_open",
            }
            response = requests.get("http://api.hh.ru/employers/", params)
            return response.json()["items"]
        else:
            for i in self.name:
                params = {
                    "per_page": 10,
                    "sort_by": "by_vacancies_open",
                    "text": i
                }
                response = requests.get("http://api.hh.ru/employers/", params)
                list_employeers.extend(response.json()["items"])

    def get_vacancies(
        self, keyword: str = "", per_page: int = 100, salary: int | None = None
    ) -> list | str:
        """
        Метод-обёртка для получения списка вакансий.
        """
        return self.__get_vacancies(keyword, per_page, salary)

    @staticmethod
    def get_vacancies_from_company(id_company) -> str:
        """
        Метод возвращающий json вакансий
        """
        params = {
            "per_page": 10,
            "employer_id": id_company,
            'only_with_salary': "true"
        }
        response = requests.get("http://api.hh.ru/vacancies/", params)
        return response.json()["items"]

    def get_all_vacancies(self) -> list:
        """
        Метод забирает список с метода get_employers_sort, и список get_vacancies_from_company
        и сортирует все вакансии по определенному id компании и складывает все в список
        :return: list
        :rtype: list
        """
        employers = self.get_request_employers()
        vacancies = []
        for employer in employers:
            vacancies.extend(self.get_vacancies_from_company(employer["id"]))
        return vacancies