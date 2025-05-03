class Vacancy:
    def __init__(self, name, url, salary, description):
        if not isinstance(name, str):
            self.name = 'Название не указано'
        else:
            self.name = name

        if not isinstance(salary, dict):
            self.salary = 'З/П не указана'
            self.salary_from = None
            self.salary_to = None
        else:
            self.salary = f'{salary["from"]}-{salary["to"]}'
            self.salary_from = salary.get('from')
            self.salary_to = salary.get('to')

        self.url = url
        self.description = description


    @classmethod
    def cast_to_object_list(cls, data_list):
        vacancies = []
        for data in data_list:
            vacancy = cls(data['name'],
                          data['url'],
                          data['salary'],
                          data['snippet']['responsibility'])
            vacancies.append(vacancy)
        return vacancies


    def __repr__(self):
        return (f"Вакансия: {self.name}\n"
                f"Зарплата: {self.salary}\n"
                f"Ссылка: {self.url}\n"
                f"Описание: {self.description}")

    @classmethod
    def get_top_n_by_salary(cls, vacancies, n=5):
        # Фильтруем вакансии с пустой зарплатой
        filtered_vacancies = []
        for vacancy in vacancies:
            if vacancy.salary_to is not None:
                filtered_vacancies.append(vacancy)
        filtered_vacancies_by_salary = sorted(filtered_vacancies,
                                 key=lambda x: x.salary_to,
                                 reverse=True)
        return filtered_vacancies_by_salary[:n]


