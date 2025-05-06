class Vacancy:
    """
    Класс для представления информации о вакансии.

    Attributes:
        name (str): Название вакансии.
        url (str): Ссылка на вакансию.
        salary (str): Диапазон зарплаты.
        description (str): Описание вакансии.
        salary_from (int | None): Минимальная зарплата.
        salary_to (int | None): Максимальная зарплата.
    """

    __slots__ = ('name', 'url', 'salary', 'description', 'salary_from', 'salary_to')

    def __init__(self, name: str, url: str, salary: dict, description: str):
        """
        Инициализация объекта Vacancy.

        Args:
            name (str): Название вакансии.
            url (str): Ссылка на вакансию.
            salary (dict): Словарь с информацией о зарплате.
            description (str): Описание вакансии.
        """
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
    def cast_to_object_list(cls, data_list: list) -> list:
        """
        Преобразование списка словарей в список объектов Vacancy.

        Args:
            data_list (list): Список словарей с информацией о вакансиях.

        Returns:
            list: Список объектов Vacancy.
        """
        vacancies = []
        for data in data_list:
            vacancy = cls(data['name'],
                          data['url'],
                          data['salary'],
                          data['snippet']['responsibility'])
            vacancies.append(vacancy)
        return vacancies

    def __repr__(self) -> str:
        """
        Строковое представление объекта Vacancy.

        Returns:
            str: Строка с информацией о вакансии.
        """
        return (f"\nВакансия: {self.name}\n"
                f"Зарплата: {self.salary}\n"
                f"Ссылка: {self.url}\n"
                f"Описание: {self.description}\n"
                f"{'_'*80}\n")

    @classmethod
    def get_top_n_by_salary(cls, vacancies: list, n: int = 5) -> list:
        """
        Получение топ-N вакансий с наибольшей зарплатой.

        Args:
            vacancies (list): Список объектов Vacancy.
            n (int): Количество вакансий для возврата.

        Returns:
            list: Список объектов Vacancy с наибольшей зарплатой.
        """
        filtered_vacancies = []
        for vacancy in vacancies:
            if vacancy.salary_to is not None:
                filtered_vacancies.append(vacancy)
        filtered_vacancies_by_salary = sorted(filtered_vacancies,
                                              key=lambda x: x.salary_to,
                                              reverse=True)
        return filtered_vacancies_by_salary[:n]

    @classmethod
    def get_vacancy_by_search_query(cls, vacancies: list, search_query: str) -> list:
        """
        Поиск вакансий по запросу.

        Args:
            vacancies (list): Список объектов Vacancy.
            search_query (str): Запрос для поиска.

        Returns:
            list: Список объектов Vacancy, соответствующих запросу.
        """
        if type(vacancies) != list:
            return f"Вакансии по названию не найдены"

        filtered_vacancies = []
        for vacancy in vacancies:
            if search_query.lower() in vacancy.name.lower():
                filtered_vacancies.append(vacancy)
            elif search_query == '':
                filtered_vacancies.append(vacancy)
        if filtered_vacancies == []:
            return f"Вакансии по названию не найдены"
        return filtered_vacancies

    @classmethod
    def get_vacancy_by_description(cls, vacancies: list, search_description: str) -> list:
        """
        Поиск вакансий по описанию.

        Args:
            vacancies (list): Список объектов Vacancy.
            search_description (str): Описание для поиска.

        Returns:
            list: Список объектов Vacancy, соответствующих описанию.
        """
        if type(vacancies) != list:
            return f"Вакансии по описанию не найдены"
        filtered_vacancies = []
        for vacancy in vacancies:
            if vacancy.description is not None:
                if search_description.lower() in vacancy.description.lower():
                    filtered_vacancies.append(vacancy)
                elif search_description == '':
                    filtered_vacancies.append(vacancy)
        if filtered_vacancies == []:
            return f"Вакансии по описанию не найдены"
        return filtered_vacancies

    def __lt__(self, other: 'Vacancy') -> bool:
        """
        Сравнение вакансий по максимальной зарплате.

        Args:
            other (Vacancy): Другая вакансия для сравнения.

        Returns:
            bool: True, если максимальная зарплата текущей вакансии меньше, чем у другой вакансии.
        """
        if self.salary_to is None or other.salary_to is None:
            return False
        return self.salary_to < other.salary_to

    def __gt__(self, other: 'Vacancy') -> bool:
        """
        Сравнение вакансий по максимальной зарплате.

        Args:
            other (Vacancy): Другая вакансия для сравнения.

        Returns:
            bool: True, если максимальная зарплата текущей вакансии больше, чем у другой вакансии.
        """
        if self.salary_to is None or other.salary_to is None:
            return False
        return self.salary_to > other.salary_to

    @classmethod
    def get_vacancies_by_salary_range(cls, vacancies: list, salary_range: str) -> list:
        """
        Фильтрация вакансий по диапазону зарплаты.

        Args:
            vacancies (list): Список объектов Vacancy.
            salary_range (str): Диапазон зарплаты в формате "от X до Y".

        Returns:
            list: Список объектов Vacancy, соответствующих диапазону зарплаты.
        """
        try:
            parts = salary_range.split()
            lower_bound = int(parts[1])
            upper_bound = int(parts[3])
        except (IndexError, ValueError):
            print("Некорректный формат диапазона зарплаты.")
            return []

        filtered_vacancies = [
            vacancy for vacancy in vacancies
            if vacancy.salary_from is not None and vacancy.salary_to is not None
               and lower_bound <= vacancy.salary_from <= upper_bound
               or lower_bound <= vacancy.salary_to <= upper_bound
        ]

        return filtered_vacancies
