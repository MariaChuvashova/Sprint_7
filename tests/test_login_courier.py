import pytest
import requests
import allure
from data import ERROR_MESSAGES, STATUS_CODES
from urls import URLs


@allure.feature("Логин курьера")
class TestLoginCourier:

    @allure.title("Тест: курьер может авторизоваться")
    def test_courier_can_login(self, create_test_courier):
        courier_data = create_test_courier

        payload = {
            "login": courier_data["login"],
            "password": courier_data["password"]
        }

        response = requests.post(URLs.LOGIN_COURIER, json=payload)
        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Тест: для авторизации нужно передать все обязательные поля")
    def test_login_requires_all_fields(self, create_test_courier):
        courier_data = create_test_courier

        payload_without_password = {"login": courier_data["login"]}
        response = requests.post(URLs.LOGIN_COURIER, json=payload_without_password)
        assert response.status_code == 400
        assert ERROR_MESSAGES["missing_login_data"] in response.json()["message"]

        payload_without_login = {"password": courier_data["password"]}
        response = requests.post(URLs.LOGIN_COURIER, json=payload_without_login)
        assert response.status_code == 400
        assert ERROR_MESSAGES["missing_login_data"] in response.json()["message"]

    @allure.title("Тест: система вернёт ошибку при неправильном логине")
    def test_login_with_wrong_login_returns_error(self, create_test_courier):
        courier_data = create_test_courier

        payload = {
            "login": "wrong_login_123",
            "password": courier_data["password"]
        }

        response = requests.post(URLs.LOGIN_COURIER, json=payload)
        assert response.status_code == 404
        assert ERROR_MESSAGES["account_not_found"] in response.json()["message"]

    @allure.title("Тест: система вернёт ошибку при неправильном пароле")
    def test_login_with_wrong_password_returns_error(self, create_test_courier):
        courier_data = create_test_courier

        payload = {
            "login": courier_data["login"],
            "password": "wrong_password_456"
        }

        response = requests.post(URLs.LOGIN_COURIER, json=payload)
        assert response.status_code == 404
        assert ERROR_MESSAGES["account_not_found"] in response.json()["message"]

    @allure.title("Тест: авторизация под несуществующим пользователем возвращает ошибку")
    def test_login_nonexistent_user_returns_error(self):
        payload = {
            "login": "nonexistent_user_789",
            "password": "nonexistent_password_789"
        }

        response = requests.post(URLs.LOGIN_COURIER, json=payload)
        assert response.status_code == 404
        assert ERROR_MESSAGES["account_not_found"] in response.json()["message"]

    @allure.title("Тест: успешный запрос возвращает id")
    def test_successful_login_returns_id(self, create_test_courier):
        courier_data = create_test_courier

        payload = {
            "login": courier_data["login"],
            "password": courier_data["password"]
        }

        response = requests.post(URLs.LOGIN_COURIER, json=payload)
        assert response.status_code == 200
        assert "id" in response.json()
        assert isinstance(response.json()["id"], int)
