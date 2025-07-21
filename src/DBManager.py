import psycopg2
import psycopg2.errors
import dotenv
import os

dotenv.load_dotenv()

class DBManager:

    """
    Класс для создания базы данных с вакансиями.
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
                print(f"Работодатель с ID {vacancy["employer"]["id"]} уже существует в базе данных")
            except KeyError as e:
                print(f"Ошибка при добавлении работодателя: {e}\n"\
                       f"У работодателя {vacancy["employer"]["name"]} нет id")

            try:
                salary_from = (
                    vacancy["salary"]["from"] if vacancy["salary"] is not None else 0
                )
                salary_to = (
                    vacancy["salary"]["to"] if vacancy["salary"] is not None else 0
                )
                self.cursor.execute(
                    """
                                INSERT INTO vacancies (id, employer_name, vacancy_name, salary_from, salary_to, currency, vacancy_url, employer_id)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            """,
                    (
                        vacancy["id"],
                        vacancy["employer"]["name"],
                        vacancy["name"],
                        salary_from,
                        salary_to,
                        vacancy["salary"]["currency"]
                        if vacancy["salary"] is not None
                        else None,
                        vacancy["alternate_url"],
                        vacancy["employer"]["id"]
                    ),
                )
            except psycopg2.errors.UniqueViolation:
                print(f"Вакансия с ID {vacancy['id']} уже существует в базе данных")
            except psycopg2.Error as e:
                print(f"Ошибка при добавлении вакансии: {e}")



    def get_all_vacancies(self):
        try:
            self.cursor.execute("""SELECT * FROM vacancies""")
            vacancies = []
            for row in self.cursor.fetchall():
                vacancies.append(
                    {
                        "id": row[0],
                        "employer_name": row[1],
                        "vacancy_name": row[2],
                        "salary": f"{row[3]} - {row[4]} {row[5]}",
                        "vacancy_url": row[6],
                    }
                )
            return vacancies
        except psycopg2.Error as e:
            print(f"Ошибка при получении вакансий: {e}")
            return []

    def get_companies_and_vacancies_count(self):
        try:
            self.cursor.execute(
                """
                SELECT employer_name, COUNT(*) as vacancies_count FROM vacancies
                GROUP BY employer_name
                ORDER BY vacancies_count DESC
                """
            )

            companies = []
            for row in self.cursor.fetchall():
                companies.append({"employer_name": row[0], "vacancies_count": row[1]})
            return companies
        except psycopg2.Error as e:
            print(f"Ошибка при получении данных о компаниях: {e}")
            return []

    def get_avg_salary(self):
        try:
            # Вычисляем среднее арифметическое между salary_from и salary_to
            self.cursor.execute(
                """SELECT AVG((salary_from + salary_to) / 2) as avg_salary FROM vacancies
            WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL"""
            )
            result = self.cursor.fetchone()
            if result:
                return result[0]
            return None
        except psycopg2.Error as e:
            print(f"Ошибка при получении средней зарплаты: {e}")
            return None

    def get_vacancies_with_higher_salary(self, avg_salary):
        try:
            self.cursor.execute(
                """
                    SELECT 
                        *
                    FROM 
                        vacancies
                    WHERE 
                        ((salary_from + salary_to) / 2) > %s
                    """,
                (avg_salary,),
            )

            vacancies = []
            for row in self.cursor.fetchall():
                vacancies.append(
                    {
                        "id": row[0],
                        "employer_name": row[1],
                        "vacancy_name": row[2],
                        "salary": f"{row[3]} - {row[4]} {row[5]}",
                        "vacancy_url": row[6],
                    }
                )

            return vacancies
        except psycopg2.Error as e:
            print(f"Ошибка при получении вакансий с зарплатой выше средней: {e}")
            return []

    def get_vacancies_with_keyword(self, keyword):
        try:
            # Формируем SQL-запрос с учетом поиска по ключевым словам
            self.cursor.execute(
                """SELECT * FROM vacancies WHERE LOWER(vacancy_name) LIKE %s""",
                ("%" + keyword.lower() + "%",),
            )

            vacancies = []
            for row in self.cursor.fetchall():
                vacancies.append(
                    {
                        "id": row[0],
                        "employer_name": row[1],
                        "vacancy_name": row[2],
                        "salary": f"{row[3]} - {row[4]} {row[5]}",
                        "vacancy_url": row[6],
                    }
                )

            return vacancies
        except psycopg2.Error as e:
            print(f"Ошибка при поиске вакансий по ключевому слову: {e}")
            return []

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


if __name__ == "__main__":
    db = DBManager(hh_emp)
    av_sal = db.get_avg_salary()
    print(av_sal)
    print(db.get_vacancies_with_keyword("Строитель"))
    print(db.get_companies_and_vacancies_count())
    print(db.get_vacancies_with_higher_salary(av_sal))
    db.close_connection()
