from abc import ABC, abstractmethod


class HeadHunterAbstract(ABC):

    @abstractmethod
    def get_vacancies(self, keyword, per_page, salary):
        pass