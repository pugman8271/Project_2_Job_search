from abc import ABC, abstractmethod


class JsonSaverAbstract(ABC):

    @abstractmethod
    def add_vacancy(self, list_info):
        pass
    def delete_vacancy(self, list_info):
        pass