import os
from typing import Any, Dict, List

import dotenv
import psycopg2
import psycopg2.errors

dotenv.load_dotenv()


class DBInicializator:
    """
    Класс для управления базой данных вакансий.

    Отвечает за создание, подключение и управление базой данных,
    а также за загрузку данных о вакансиях.
    """

    def __init__(
        self, vacancies_list: List[Dict[str, Any]], db_name: str = "hh_vacancies"
    ) -> None:
        """
        Инициализация класса.

        :param vacancies_list: Список вакансий для загрузки в БД
        :param db_name: Имя базы данных (по умолчанию "hh_vacancies")
        """
        self.db_name = db_name
        self.vacancies_list = vacancies_list
        self.create_db()
        self.connection = self.connect_db()
        self.cursor = self.connection.cursor()
        self.create_table()

    def close_connection(self) -> None:
        """
        Закрывает соединение с базой данных.

        Выполняет корректное закрытие курсора и соединения.
        """
        self.cursor.close()
        self.connection.close()

    def connect_db(self) -> psycopg2.connect:
        """
        Устанавливает соединение с базой данных.

        :return: Объект соединения с БД
        """
        connection = psycopg2.connect(
            dbname=self.db_name,
            user=os.getenv("DB_NAME"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
        connection.autocommit = True
        return connection

    def create_db(self) -> None:
        """
        Создает новую базу данных.

        Выполняет удаление существующей БД (если есть) и создает новую.
        """
        connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_NAME"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
        connection.autocommit = True
        try:
            cursor = connection.cursor()
            cursor.execute(f"DROP DATABASE IF EXISTS {self.db_name}")
            cursor.execute(f"CREATE DATABASE {self.db_name}")
        except psycopg2.Error as e:
            print(f"Произошла ошибка при создании БД: {e}")
        finally:
            connection.close()

    def create_table(self) -> None:
        """
        Создает таблицы в базе данных.

        Создает две таблицы: employer и vacancies,
        а также загружает данные из списка вакансий.
        """
        self.connection.autocommit = True
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS employer (
                id VARCHAR(255) PRIMARY KEY,
                employer_name VARCHAR(255)
            );
            CREATE TABLE IF NOT EXISTS vacancies (
                id VARCHAR(255) PRIMARY KEY,
                employer_name VARCHAR(255),
                vacancy_name VARCHAR(255),
                salary_from INTEGER,
                salary_to INTEGER,
                currency VARCHAR(10),
                vacancy_url VARCHAR(255),
                employer_id VARCHAR(255),
                FOREIGN KEY (employer_id) REFERENCES employer(id)
            )"""
        )

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
                salary_from = (
                    vacancy["salary"]["from"] if vacancy["salary"] is not None else 0
                )
                salary_to = (
                    vacancy["salary"]["to"] if vacancy["salary"] is not None else 0
                )
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
                        (
                            vacancy["salary"]["currency"]
                            if vacancy["salary"] is not None
                            else None
                        ),
                        vacancy["alternate_url"],
                        vacancy["employer"]["id"],
                    ),
                )
            except psycopg2.errors.UniqueViolation:
                print(f"Вакансия с ID {vacancy['id']} уже существует в базе данных")
            except psycopg2.Error as e:
                print(f"Ошибка при добавлении вакансии: {e}")
