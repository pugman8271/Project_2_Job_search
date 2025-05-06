from src.vacancy import Vacancy


def test_init_vacancy_with_valid_data(new_vacancy_developer):
    assert new_vacancy_developer.name == "Python Developer"
    assert new_vacancy_developer.url == "<https://hh.ru/vacancy/123456>"
    assert new_vacancy_developer.salary == "300000-350000"
    assert new_vacancy_developer.description == "Требования: опыт работы от 3 лет..."


def test_init_vacancy_with_single_salary(new_vacancy_driver):
    assert new_vacancy_driver.name == "Водитель"
    assert new_vacancy_driver.url == "<https://hh.ru/vacancy/12348755456>"
    assert new_vacancy_driver.salary == "200000-26000"
    assert new_vacancy_driver.description == "Требования: опыт работы от 6 лет водителем"


def test_cast_to_object_list(vacancy_list):
    data_list = [
        {
            "name": "Python Developer",
            "url": "<https://hh.ru/vacancy/123456>",
            "salary": {"from": 300000, "to": 350000},
            "snippet": {"responsibility": "Требования: опыт работы от 3 лет..."}
        },
        {
            "name": "Водитель",
            "url": "<https://hh.ru/vacancy/12348755456>",
            "salary": {"from": 200000, "to": 26000},
            "snippet": {"responsibility": "Требования: опыт работы от 6 лет водителем"}
        }
    ]
    casted_vacancies = Vacancy.cast_to_object_list(data_list)
    assert len(casted_vacancies) == len(vacancy_list)
    for i in range(len(vacancy_list)):
        assert casted_vacancies[i].name == vacancy_list[i].name
        assert casted_vacancies[i].url == vacancy_list[i].url
        assert casted_vacancies[i].salary == vacancy_list[i].salary
        assert casted_vacancies[i].description == vacancy_list[i].description
        assert casted_vacancies[i].salary_from == vacancy_list[i].salary_from
        assert casted_vacancies[i].salary_to == vacancy_list[i].salary_to


def test_get_top_n_by_salary(vacancy_list):
    top_vacancies = Vacancy.get_top_n_by_salary(vacancy_list, n=2)
    assert top_vacancies[0].name == "Python Developer"
    assert top_vacancies[1].name == "Водитель"


def test_get_vacancy_by_keyword(vacancy_list):
    keywords = ["Python"]
    filtered_vacancies = Vacancy.get_vacancy_by_keyword(vacancy_list, keywords)
    assert filtered_vacancies == [vacancy_list[0]]


def test_get_vacancy_by_keyword_empty_keywords(vacancy_list):
    keywords = []
    filtered_vacancies = Vacancy.get_vacancy_by_keyword(vacancy_list, keywords)
    assert filtered_vacancies == vacancy_list


def test_get_vacancy_by_keyword_no_matches(vacancy_list):
    keywords = ["Неизвестная профессия"]
    filtered_vacancies = Vacancy.get_vacancy_by_keyword(vacancy_list, keywords)
    assert filtered_vacancies == 'Вакансии по ключевым словам не найдены'


def test_get_vacancies_by_salary_range(vacancy_list):
    salary_range = '0-200000'
    filtered_vacancies = Vacancy.get_vacancies_by_salary_range(vacancy_list, salary_range)
    assert filtered_vacancies == [vacancy_list[1]]
