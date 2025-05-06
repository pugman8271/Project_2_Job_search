from abc import ABC, abstractmethod

class HeadHunterAbstract(ABC):
    """
    Абстрактный класс для работы с API HeadHunter.

    Методы:
    get_vacancies(keyword, per_page, salary): получает список вакансий с HeadHunter.
    """

    @abstractmethod
    def get_vacancies(self, keyword, per_page, salary):
        """
        Получает список вакансий с HeadHunter.

        Args:
        keyword (str): поисковый запрос.
        per_page (int): количество вакансий на странице.
        salary (int): зарплата.
        """
        pass
