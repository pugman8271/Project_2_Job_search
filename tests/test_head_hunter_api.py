
from unittest.mock import patch, Mock
from src.HeadHunter_api import HeadHunterAPI

def test_get_vacancies_success():
    api = HeadHunterAPI()
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'items': ['vacancy1', 'vacancy2']}
        mock_get.return_value = mock_response
        result = api.get_vacancies(keyword='python', per_page=2, salary=100000)
        assert result == ['vacancy1', 'vacancy2']

def test_get_vacancies_error():
    api = HeadHunterAPI()
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        result = api.get_vacancies()
        assert isinstance(result, str)
        assert result.startswith('Запрос не выполнен, ошибка:')


