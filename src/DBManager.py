from typing import Any, Dict, List, Optional

import psycopg2
import psycopg2.errors

from src.DBInicializator import DBInicializator


class DBManager(DBInicializator):
    """
    Класс для редактирования и управления базой данных с вакансиями.

    Предоставляет методы для работы с данными о вакансиях, включая:
    - Получение всех вакансий
    - Подсчет вакансий по компаниям
    - Расчет средней зарплаты
    - Поиск вакансий с зарплатой выше средней
    - Поиск вакансий по ключевому слову
    """

    def __init__(self, vacancies_list: List[Dict[str, Any]]) -> None:
        """
        Инициализация менеджера базы данных.
        :param vacancies_list: Список вакансий для загрузки в БД
        """
        super().__init__(vacancies_list)
        self.vacancies_list = vacancies_list

        for vacancy in self.vacancies_list:
            try:
                self.cursor.execute(
                    "INSERT INTO employer (id, employer_name) VALUES (%s, %s)",
                    (vacancy["employer"]["id"], vacancy["employer"]["name"]),
                )
            except psycopg2.errors.UniqueViolation:
                print(
                    f"Работодатель с ID {vacancy['employer']['id']} уже существует в базе данных"
                )
            except KeyError as e:
                print(
                    f"Ошибка при добавлении работодателя: {e}\nУ работодателя {vacancy['employer']['name']} нет id"
                )

            try:
                salary_from = vacancy["salary"]["from"] if vacancy["salary"] else 0
                salary_to = vacancy["salary"]["to"] if vacancy["salary"] else 0
                self.cursor.execute(
                    "INSERT INTO vacancies "
                    "(id, employer_name, vacancy_name, salary_from, salary_to, currency, vacancy_url, employer_id) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (
                        vacancy["id"],
                        vacancy["employer"]["name"],
                        vacancy["name"],
                        salary_from,
                        salary_to,
                        vacancy["salary"]["currency"] if vacancy["salary"] else None,
                        vacancy["alternate_url"],
                        vacancy["employer"]["id"],
                    ),
                )
            except psycopg2.errors.UniqueViolation:
                print(f"Вакансия с ID {vacancy['id']} уже существует в базе данных")
            except psycopg2.Error as e:
                print(f"Ошибка при добавлении вакансии: {e}")

    def get_all_vacancies(self) -> List[Dict[str, Any]]:
        """
        Получает все вакансии из базы данных.

        :return: Список словарей с информацией о вакансиях
        """
        try:
            self.cursor.execute("SELECT * FROM vacancies")
            return [
                {
                    "id": row[0],
                    "employer_name": row[1],
                    "vacancy_name": row[2],
                    "salary": f"{row[3]} - {row[4]} {row[5]}",
                    "vacancy_url": row[6],
                }
                for row in self.cursor.fetchall()
            ]
        except psycopg2.Error as e:
            print(f"Ошибка при получении вакансий: {e}")
            return []

    def get_companies_and_vacancies_count(self) -> List[Dict[str, int]]:
        """
        Получает список компаний с количеством их вакансий.

        :return: Список словарей с названиями компаний и количеством вакансий
        """
        try:
            self.cursor.execute(
                "SELECT employer_name, COUNT(*) as vacancies_count "
                "FROM vacancies GROUP BY employer_name ORDER BY vacancies_count DESC"
            )
            return [
                {"employer_name": row[0], "vacancies_count": row[1]}
                for row in self.cursor.fetchall()
            ]
        except psycopg2.Error as e:
            print(f"Ошибка при получении данных о компаниях: {e}")
            return []

    def get_avg_salary(self) -> Optional[float]:
        """
        Рассчитывает среднюю зарплату по всем вакансиям.

        :return: Средняя зарплата или None при ошибке
        """
        try:
            self.cursor.execute(
                "SELECT AVG((salary_from + salary_to) / 2) as avg_salary "
                "FROM vacancies WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL"
            )
            result = self.cursor.fetchone()
            return result[0] if result else None
        except psycopg2.Error as e:
            print(f"Ошибка при получении средней зарплаты: {e}")
            return None

    def get_vacancies_with_higher_salary(
        self, avg_salary: float
    ) -> List[Dict[str, Any]]:
        """
        Поиск вакансий с заработной платой выше средней.

        :return: Список словарей с информацией о вакансиях
        """
        try:
            self.cursor.execute(
                "SELECT * FROM vacancies WHERE ((salary_from + salary_to) / 2) > %s",
                (avg_salary,),
            )
            return [
                {
                    "id": row[0],
                    "employer_name": row[1],
                    "vacancy_name": row[2],
                    "salary": f"{row[3]} - {row[4]} {row[5]}",
                    "vacancy_url": row[6],
                }
                for row in self.cursor.fetchall()
            ]
        except psycopg2.Error as e:
            print(f"Ошибка при получении вакансий с зарплатой выше средней: {e}")
            return []

    def get_vacancies_with_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Поиск вакансий по ключевому слову.

        :return: Список словарей с информацией о вакансиях
        """
        try:
            self.cursor.execute(
                "SELECT * FROM vacancies WHERE LOWER(vacancy_name) LIKE %s",
                ("%" + keyword.lower() + "%",),
            )
            return [
                {
                    "id": row[0],
                    "employer_name": row[1],
                    "vacancy_name": row[2],
                    "salary": f"{row[3]} - {row[4]} {row[5]}",
                    "vacancy_url": row[6],
                }
                for row in self.cursor.fetchall()
            ]
        except psycopg2.Error as e:
            print(f"Ошибка при поиске вакансий по ключевому слову: {e}")
            return []
