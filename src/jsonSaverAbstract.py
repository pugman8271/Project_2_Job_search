from abc import ABC, abstractmethod


class JsonSaverAbstract(ABC):

    @abstractmethod
    def delete_vacancy(self, list_info):
        pass