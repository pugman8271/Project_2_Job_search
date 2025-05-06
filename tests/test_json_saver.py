import pytest
from pathlib import Path
from src.jsonSaverAbstract import JsonSaverAbstract
from src.json_saver import JSONSaver
from src.vacancy import Vacancy
import json
json_saver = JSONSaver('data/json_data_test.json')

def test_add_vacancy(new_vacancy_developer):
    json_saver.add_vacancy(new_vacancy_developer)
    with open(json_saver._file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    assert len(data) == 1
    assert data[0]['name'] == new_vacancy_developer.name
    assert data[0]['url'] == new_vacancy_developer.url
    assert data[0]['salary'] == new_vacancy_developer.salary
    assert data[0]['description'] == new_vacancy_developer.description

def test_add_duplicate_vacancy(new_vacancy_driver):
    json_saver.add_vacancy(new_vacancy_driver)
    json_saver.add_vacancy(new_vacancy_driver)  # Попытка добавить дублирующуюся вакансию
    with open(json_saver._file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    assert len(data) == 2
    assert data[1]['name'] == new_vacancy_driver.name
    assert data[1]['url'] == new_vacancy_driver.url
    assert data[1]['salary'] == new_vacancy_driver.salary
    assert data[1]['description'] == new_vacancy_driver.description

def test_delete_vacancy(new_vacancy_developer):
    json_saver.add_vacancy(new_vacancy_developer)
    json_saver.delete_vacancy(new_vacancy_developer)
    with open(json_saver._file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    assert len(data) == 1

    # Перезаписываем файл, чтобы тесты проходили
    with open(json_saver._file_path, 'w', encoding='utf-8') as file:
        data = []

