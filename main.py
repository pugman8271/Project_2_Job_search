from src.HeadHunter_api import HeadHunterAPI
from src.json_saver import JSONSaver
from src.vacancy import Vacancy


# Создание экземпляра класса для работы с API сайтов с вакансиями
hh_api = HeadHunterAPI()
# Передаем пусть, по которому будем сохранять отфильтрованные вакансии
json_saver = JSONSaver("data/json_data.json")
hh_vacancies = hh_api.get_vacancies()

hh_emp = hh_api.get_all_vacancies()

vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)
def user_interaction():
    print("HeadHunter")
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат: ")
    json_save = input(
        "Сохранить найденные вакансии в JSON файле?\n" "Введите да или нет:"
    )
    # Получение вакансий с hh.ru в формате JSON
    hh_vacancies = hh_api.get_vacancies(search_query)
    # Преобразование набора данных из JSON в список объектов
    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)
    # Фильтруемся по ключевым словам пользователя
    filtered_vacancies = Vacancy.get_vacancy_by_keyword(vacancies_list, filter_words)
    # Фильтруемся по диапозону зарплаты
    ranged_vacancies = Vacancy.get_vacancies_by_salary_range(
        filtered_vacancies, salary_range
    )
    # Фильтруем топ-N вакансий по заданным параметрам выше
    top_vacancies = Vacancy.get_top_n_by_salary(ranged_vacancies, top_n)

    # Выводим вакансии в консоль по запросу пользователя
    print(top_vacancies)

    # Сохраняем вакансии по запросу в файл
    if json_save.lower() == "да":
        for vacancy in top_vacancies:
            json_saver.add_vacancy(vacancy)


# print(hh_emp)
# if __name__ == "__main__":
#     user_interaction()
# DataBaseHH(vacancies_list, 'Vac', 'Aslan', '9308271')

