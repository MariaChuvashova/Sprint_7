import pytest
import requests
import allure
import random
from data import ERROR_MESSAGES, STATUS_CODES, COURIER_TEST_DATA
from urls import URLs


@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Тест: курьера можно создать")
    def test_courier_can_be_created(self, cleanup_courier):
        # Генерируем уникальные данные для курьера
        login = f"testuser_{random.randint(1000, 9999)}"
        password = f"password_{random.randint(1000, 9999)}"
        first_name = f"name_{random.randint(1000, 9999)}"
        
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        
        # Шаг создания курьера
        with allure.step("Создать нового курьера"):
            response = requests.post(URLs.CREATE_COURIER, json=payload)
        
        # Проверяем, что курьер создан успешно
        assert response.status_code == 201
        assert response.json()["ok"] == True
        
        # Логинимся, чтобы получить ID и добавить в cleanup
        with allure.step("Получить ID курьера для очистки"):
            login_payload = {"login": login, "password": password}
            login_response = requests.post(URLs.LOGIN_COURIER, json=login_payload)
            courier_id = login_response.json().get("id")
            cleanup_courier.append(courier_id)

    @allure.title("Тест: нельзя создать двух одинаковых курьеров")
    def test_cannot_create_duplicate_courier(self, create_duplicate_courier_data):
        courier_data = create_duplicate_courier_data

        with allure.step("Попытаться создать второго курьера с тем же логином"):
            payload = {
                "login": courier_data["login"],
                "password": "different_password_123",
                "firstName": "Другойкурьер"
            }
            response = requests.post(URLs.CREATE_COURIER, json=payload)
        
        assert response.status_code == STATUS_CODES['conflict']
        assert ERROR_MESSAGES["login_exists"] in response.json()["message"]

    @allure.title("Тест: создание курьера без логина возвращает ошибку")
    def test_create_courier_without_login_returns_error(self):
        payload = COURIER_TEST_DATA["missing_login"]

        with allure.step("Отправить запрос создания курьера без логина"):
            response = requests.post(URLs.CREATE_COURIER, json=payload)
        
        assert response.status_code == STATUS_CODES['bad_request']
        assert ERROR_MESSAGES["missing_required_field"] in response.json()["message"]

    @allure.title("Тест: создание курьера без пароля возвращает ошибку")
    def test_create_courier_without_password_returns_error(self):
        payload = COURIER_TEST_DATA["missing_password"]

        with allure.step("Отправить запрос создания курьера без пароля"):
            response = requests.post(URLs.CREATE_COURIER, json=payload)
        
        assert response.status_code == STATUS_CODES['bad_request']
        assert ERROR_MESSAGES["missing_required_field"] in response.json()["message"]

    @allure.title("Тест: успешный запрос возвращает правильный код ответа")
    def test_successful_request_returns_correct_code(self, cleanup_courier):
        login = f"testuser_{random.randint(1000, 9999)}"
        password = f"password_{random.randint(1000, 9999)}"
        first_name = f"name_{random.randint(1000, 9999)}"
        
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        
        with allure.step("Создать нового курьера"):
            response = requests.post(URLs.CREATE_COURIER, json=payload)
        
        assert response.status_code == 201
        
        # Добавляем в cleanup
        with allure.step("Добавить курьера в cleanup"):
            login_payload = {"login": login, "password": password}
            login_response = requests.post(URLs.LOGIN_COURIER, json=login_payload)
            courier_id = login_response.json().get("id")
            cleanup_courier.append(courier_id)

    @allure.title("Тест: создание курьера с существующим логином возвращает ошибку")
    def test_create_courier_with_existing_login_returns_error(self, create_duplicate_courier_data):
        courier_data = create_duplicate_courier_data

        with allure.step("Попытаться создать курьера с существующим логином"):
            payload = {
                "login": courier_data["login"],
                "password": "different_password_123",
                "firstName": "Другойкурьер"
            }
            response = requests.post(URLs.CREATE_COURIER, json=payload)
        
        assert response.status_code == STATUS_CODES['conflict']
        assert ERROR_MESSAGES["login_exists"] in response.json()["message"]
