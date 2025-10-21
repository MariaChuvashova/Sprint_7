import pytest
import requests
import allure
from data import ERROR_MESSAGES, STATUS_CODES, COURIER_TEST_DATA
from urls import URLs


@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Тест: курьера можно создать")
    def test_courier_can_be_created(self, create_test_courier):
        assert create_test_courier["id"] is not None

    @allure.title("Тест: нельзя создать двух одинаковых курьеров")
    def test_cannot_create_duplicate_courier(self, create_duplicate_courier_data):
        courier_data = create_duplicate_courier_data

        with allure.step("Попытаться создать второго курьера с тем же логином"):
            payload = {
                "login": courier_data["login"],
                "password": "different_password_123",
                "firstName": "ДругойКурьер"
            }

            response = requests.post(URLs.CREATE_COURIER, json=payload)
            assert response.status_code == STATUS_CODES["conflict"]
            assert ERROR_MESSAGES["login_exists"] in response.json()["message"]

    @allure.title("Тест: создание курьера без логина возвращает ошибку")
    def test_create_courier_without_login_returns_error(self):
        payload = COURIER_TEST_DATA["missing_login"]
        
        response = requests.post(URLs.CREATE_COURIER, json=payload)
        assert response.status_code == STATUS_CODES["bad_request"]
        assert ERROR_MESSAGES["missing_data"] in response.json()["message"]

    @allure.title("Тест: создание курьера без пароля возвращает ошибку")
    def test_create_courier_without_password_returns_error(self):
        payload = COURIER_TEST_DATA["missing_password"]
        
        response = requests.post(URLs.CREATE_COURIER, json=payload)
        assert response.status_code == STATUS_CODES["bad_request"]
        assert ERROR_MESSAGES["missing_data"] in response.json()["message"]

    @allure.title("Тест: успешный запрос возвращает правильный код ответа")
    def test_successful_request_returns_correct_code(self, create_test_courier):
        assert create_test_courier["id"] is not None

    @allure.title("Тест: создание курьера с существующим логином возвращает ошибку")
    def test_create_courier_with_existing_login_returns_error(self, create_duplicate_courier_data):
        courier_data = create_duplicate_courier_data

        with allure.step("Попытаться создать второго курьера с тем же логином"):
            payload = {
                "login": courier_data["login"],
                "password": "another_password_456",
                "firstName": "ЕщеОдинКурьер"
            }

            response = requests.post(URLs.CREATE_COURIER, json=payload)
            assert response.status_code == STATUS_CODES["conflict"]
            assert ERROR_MESSAGES["login_exists"] in response.json()["message"]
