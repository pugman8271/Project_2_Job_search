from abc import ABC, abstractmethod


class JsonSaverAbstract(ABC):
    """
    Абстрактный класс для работы с JSON-файлами.

    Методы:
    delete_vacancy(list_info): удаляет вакансию из JSON-файла.
    """

    @abstractmethod
    def delete_vacancy(self, list_info):
        """
        Удаляет вакансию из JSON-файла.

        Args:
        list_info: информация о вакансии для удаления.
        """
        pass
