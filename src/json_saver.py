from src.jsonSaverAbstract import JsonSaverAbstract
import json

class JSONSaver(JsonSaverAbstract):
    """
    Класс для сохранения и удаления вакансий в JSON-файл.

    Attributes:
        _file_path (str): Путь к файлу для сохранения данных.
    """

    def __init__(self, file_path: str):
        """
        Инициализация объекта JSONSaver.

        Args:
            file_path (str): Путь к файлу для сохранения данных.
        """
        self._file_path = file_path

    def add_vacancy(self, vacancy: 'Vacancy') -> None:
        """
        Добавляет вакансию в JSON-файл, если её ещё нет в файле.

        Args:
            vacancy (Vacancy): Объект вакансии для добавления.
        """
        vacancy_dict = {
            "name": vacancy.name,
            "url": vacancy.url,
            "salary": vacancy.salary,
            "description": vacancy.description
        }

        try:
            with open(self._file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            if not isinstance(data, list):
                data = [data]
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        # Проверка на наличие дублирующейся вакансии по URL
        if any(v['url'] == vacancy.url for v in data):
            print(f"Данная вакансия уже есть в файле: {vacancy.url}")
            return

        data.append(vacancy_dict)

        with open(self._file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
            print(f"Данные успешно сохранены в {self._file_path}")

    def delete_vacancy(self, vacancy: 'Vacancy') -> None:
        """
        Удаляет вакансию из JSON-файла по URL.

        Args:
            vacancy (Vacancy): Объект вакансии для удаления.
        """
        vacancy_dict = {
            "name": vacancy.name,
            "url": vacancy.url,
            "salary": vacancy.salary,
            "description": vacancy.description
        }

        try:
            with open(self._file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            if not isinstance(data, list):
                data = [data]

            initial_length = len(data)
            data = [v for v in data if v['url'] != vacancy_dict['url']]

            if len(data) < initial_length:
                with open(self._file_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=2)
                    print(f'Вакансия {vacancy.name} успешно удалена из {self._file_path}')
            else:
                print(f'Вакансия {vacancy.name} не найдена в {self._file_path}')

        except (FileNotFoundError, json.JSONDecodeError):
            print(f'Файл {self._file_path} не найден или пуст')
