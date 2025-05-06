import pytest

from src.vacancy import Vacancy


@pytest.fixture
def new_vacancy_developer():
    return Vacancy(
        "Python Developer",
        "<https://hh.ru/vacancy/123456>",
        {"from": 300000, "to": 350000},
        "Требования: опыт работы от 3 лет...",
    )


@pytest.fixture
def new_vacancy_driver():
    return Vacancy(
        "Водитель",
        "<https://hh.ru/vacancy/12348755456>",
        {"from": 200000, "to": 26000},
        "Требования: опыт работы от 6 лет водителем",
    )


@pytest.fixture
def vacancy_list():
    return [
        Vacancy(
            "Python Developer",
            "<https://hh.ru/vacancy/123456>",
            {"from": 300000, "to": 350000},
            "Требования: опыт работы от 3 лет...",
        ),
        Vacancy(
            "Водитель",
            "<https://hh.ru/vacancy/12348755456>",
            {"from": 200000, "to": 26000},
            "Требования: опыт работы от 6 лет водителем",
        ),
    ]
