from abc import ABC, abstractmethod


class HeadHunterAbstract(ABC):
    """
    Абстрактный класс для работы с API HeadHunter.
    """

    @abstractmethod
    def get_vacancies(self, keyword, per_page, salary):
        """
        Получает список вакансий с HeadHunter.
        """
        pass
