import os
import dotenv
import psycopg2
import psycopg2.errors

dotenv.load_dotenv()


class DBInicializator:
    """
    Класс для создания, подключения и отключения к базам данных с вакансиями.
    """

    def __init__(self, vacancies_list, db_name="hh_vacancies"):
        self.db_name = db_name
        self.vacancies_list = vacancies_list
        self.create_db()
        self.connection = self.connect_db()
        self.cursor = self.connection.cursor()
        self.create_table()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    def connect_db(self):
        connection = psycopg2.connect(
            dbname=self.db_name,
            user="postgres",
            password=os.getenv("DB_PASSWORD"),
            host="localhost",
            port="5432",
        )
        connection.autocommit = True
        return connection

    def create_table(self):
        self.connection.autocommit = True
        self.cursor.execute(
            """
                    CREATE TABLE IF NOT EXISTS employer (
                    id VARCHAR(255) PRIMARY KEY,
                    employer_name VARCHAR(255));
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
                    )
                    """
        )

        for vacancy in self.vacancies_list:

            try:
                self.cursor.execute(
                    """
                                INSERT INTO employer (id, employer_name)
                                VALUES (%s, %s)
                            """,
                    (
                        vacancy["employer"]["id"],
                        vacancy["employer"]["name"],
                    ),
                )
            except psycopg2.errors.UniqueViolation:
                print(
                    f"Работодатель с ID {vacancy["employer"]["id"]} уже существует в базе данных"
                )
            except KeyError as e:
                print(
                    f"Ошибка при добавлении работодателя: {e}\n"
                    f"У работодателя {vacancy["employer"]["name"]} нет id"
                )
            try:
                salary_from = (
                    vacancy["salary"]["from"] if vacancy["salary"] is not None else 0
                )
                salary_to = (
                    vacancy["salary"]["to"] if vacancy["salary"] is not None else 0
                )
                self.cursor.execute(
                    """
                                INSERT INTO vacancies (id, employer_name, vacancy_name,
                                salary_from, salary_to, currency, vacancy_url, employer_id)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            """,
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



    def create_db(self):
        connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password=os.getenv("DB_PASSWORD"),
            host="localhost",
            port="5432",
        )
        connection.autocommit = True
        try:
            cursor = connection.cursor()
            cursor.execute(f"DROP DATABASE IF EXISTS {self.db_name}")
            cursor.execute(f"CREATE DATABASE {self.db_name}")
        except psycopg2.Error as e:
            print(f"{e}")
        finally:
            connection.close()
