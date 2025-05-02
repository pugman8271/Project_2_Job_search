from src.jsonSaverAbstract import JsonSaverAbstract
import json


class JSONSaver(JsonSaverAbstract):
    file_path = 'data/json_data.json'

    def add_vacancy(self, vacancy):
        vacancy_dict = {
            "name": vacancy.name,
            "url": vacancy.url,
            "salary": vacancy.salary,
            "description": vacancy.description
        }

        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            if not isinstance(data, list):
                data = [data]
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        data.append(vacancy_dict)

        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
            print(f"Данные успешно сохранены в {self.file_path}")

    def delete_vacancy(self, vacancy):
        vacancy_dict = {
            "name": vacancy.name,
            "url": vacancy.url,
            "salary": vacancy.salary,
            "description": vacancy.description
        }

        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            if not isinstance(data, list):
                data = [data]

            initial_length = len(data)
            data = [v for v in data if v['url'] != vacancy_dict['url']]

            if len(data) < initial_length:
                with open(self.file_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=2)
                    print(f'Вакансия {vacancy.name} успешно удалена из {self.file_path}')
            else:
                print(f'Вакансия {vacancy.name} не найдена в {self.file_path}')

        except (FileNotFoundError, json.JSONDecodeError):
            print(f'Файл {self.file_path} не найден или пуст')

