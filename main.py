from src.HeadHunter_api import HeadHunterAPI
from src.vacancy import Vacancy
from src.json_saver import JSONSaver
# Создание экземпляра класса для работы с API сайтов с вакансиями
hh_api = HeadHunterAPI()

# Получение вакансий с hh.ru в формате JSON
hh_vacancies = hh_api.get_vacancies("")
# Преобразование набора данных из JSON в список объектов
vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)
# Передаем пусть, по которому будем сохранять отфильтрованные вакансии
json_saver = JSONSaver('data/json_data.json')

def user_interaction():
    print('HeadHunter')
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат: ")
















# top_vacancies_s = Vacancy.get_top_n_by_salary(vacancies_list, 50)
# top_vacancies = Vacancy.get_vacancy_by_search_query(top_vacancies_s, '')
# top_vacancies_в = Vacancy.get_vacancy_by_description(top_vacancies,'')
#
#
# for i in vacancies_list:
#     json_saver.add_vacancy(i)
#     print(i)




