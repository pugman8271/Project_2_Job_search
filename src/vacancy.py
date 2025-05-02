class Vacancy:
    def __init__(self, name, url, salary, description):
        self.name = name
        self.url = url
        self.salary = salary
        self.description = description


    @classmethod
    def cast_to_object_list(cls, data_list):
        vacancies = []
        for data in data_list:
            vacancy = cls(data.get('name'),
                          data.get('url'),
                          data.get('salary'),
                          data.get('description'))
            vacancies.append(vacancy)
        return vacancies

    def __str__(self):
        return (f"Вакансия: {self.name}\n"
                f"Зарплата: {self.salary}\n"
                f"Ссылка: {self.url}\n"
                f"Описание {self.description}")
