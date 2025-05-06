from abc import ABC, abstractmethod


class JsonSaverAbstract(ABC):
    """
    Абстрактный класс для работы с JSON-файлами.
    """

    @abstractmethod
    def delete_vacancy(self, list_info):
        """
        Удаляет вакансию из JSON-файла.
        """
        pass
