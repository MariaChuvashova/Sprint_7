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
        
        with allure.step("Отправить запрос на авторизацию курьера"):
            response = requests.post(URLs.LOGIN_COURIER, json=payload)
        
        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Тест: для авторизации нужно передать логин")
    def test_login_requires_login(self, create_test_courier):
        courier_data = create_test_courier
        
        payload_without_login = {"password": courier_data["password"]}
        
        with allure.step("Отправить запрос на авторизацию без логина"):
            response = requests.post(URLs.LOGIN_COURIER, json=payload_without_login)
        
        assert response.status_code == 400
        assert ERROR_MESSAGES["missing_login_data"] in response.json()["message"]

    @allure.title("Тест: для авторизации нужно передать пароль")
    def test_login_requires_password(self, create_test_courier):
        courier_data = create_test_courier
        
        payload_without_password = {"login": courier_data["login"]}
        
        with allure.step("Отправить запрос на авторизацию без пароля"):
            response = requests.post(URLs.LOGIN_COURIER, json=payload_without_password)
        
        assert response.status_code == 400
        assert ERROR_MESSAGES["missing_login_data"] in response.json()["message"]

    @allure.title("Тест: система вернёт ошибку при неправильном логине")
    def test_login_with_wrong_login_returns_error(self, create_test_courier):
        courier_data = create_test_courier
        
        payload = {
            "login": "wrong_login_123",
            "password": courier_data["password"]
        }
        
        with allure.step("Отправить запрос с неправильным логином"):
            response = requests.post(URLs.LOGIN_COURIER, json=payload)
        
        assert response.status_code == STATUS_CODES['not_found']
        assert ERROR_MESSAGES["account_not_found"] in response.json()["message"]

    @allure.title("Тест: система вернёт ошибку при неправильном пароле")
    def test_login_with_wrong_password_returns_error(self, create_test_courier):
        courier_data = create_test_courier
        
        payload = {
            "login": courier_data["login"],
            "password": "wrong_password_123"
        }
        
        with allure.step("Отправить запрос с неправильным паролем"):
            response = requests.post(URLs.LOGIN_COURIER, json=payload)
        
        assert response.status_code == STATUS_CODES['not_found']
        assert ERROR_MESSAGES["account_not_found"] in response.json()["message"]
